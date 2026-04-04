from resources.models import Unit, Inventory, Availability
from rest_framework.exceptions import ValidationError
from incidents.models import AllocationDecision, Incident
from responders.models import Responder, Load
from django.db.models import F
from scheduler.models import Cycle, IncidentList, DecisionRecord
from django.utils import timezone

def manual_assign(incident, unit_id, inventory_id, user):
  unit = Unit.objects.filter(id=unit_id)
  unit = unit.first()
  if not unit:
    raise ValidationError('the unit is not pres.')

  invent = Inventory.objects.filter(id=inventory_id)
  invent = invent.first()
  if not invent:
    raise ValidationError('the invent is not pres.')
  if not invent.resources.filter(id=unit_id).exists():
    raise ValidationError('the unit is not pres.')
  decision = AllocationDecision.objects.create(incident=incident, unit=unit, inventory=invent, allocated_by=user)
  return decision

def suggest_responders():
  respon = Responder.objects.all()
  respon = respon.filter(loads__load_count__lt=F('max_load'))
  respon = respon.order_by('loads__load_count')
  return respon

def suggest_resources(incident):
  avail_kinds = Availability.objects.filter(location=incident.location, avail_units__gt=0).values_list('res_kind', flat=True)
  units = Unit.objects.filter(kind__in=avail_kinds)
  inventories = Inventory.objects.filter(location=incident.location, resources__in=units)
  inventories = inventories.distinct()
  return {'units': units, 'inventories': inventories}

def run_cycle():
  cycle = Cycle.objects.create()
  incidents = Incident.objects.filter(status = 'active')
  list_data = []
  
  for incid in incidents:
    priority = incid.severity + incid.prior
    list_data.append((incid, priority))
  list_data.sort(key=lambda x: x[1], reverse=True)
  IncidentList.objects.all().delete()
  
  index = 0
  for item in list_data:
    incid = item[0]
    priority = item[1]
    IncidentList.objects.create(incident=incid, prior=priority, position=index)
    index += 1

  decis_count = 0
  for incid, priority in list_data:
    avail = Availability.objects.filter(location=incid.location, avail_units__gt=0)
    avail = avail.first()
    if not avail:
      continue

    unit = Unit.objects.filter(kind=avail.res_kind)
    unit = unit.first()
    respon = Responder.objects.filter(loads__load_count__lt=F('max_load'))
    respon = respon.first()
    if not respon:
      continue
        
    AllocationDecision.objects.create(incident=incid, unit=unit, allocated_by=None)
    avail.avail_units -= 1
    avail.save()
    load, _ = Load.objects.get_or_create(responder=respon, incident=incid)
    load.load_count += 1
    load.save()

    DecisionRecord.objects.create(cycle=cycle, incident=incid, unit=unit, responder=respon, reason = 'making alloca. auto.')
    decis_count += 1
  cycle.completed_at = timezone.now()
  cycle.total_incids = len(list_data)
  cycle.decis_made = decis_count
  cycle.save()

  return cycle
