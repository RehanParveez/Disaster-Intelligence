from resources.models import Unit, Inventory, Availability
from rest_framework.exceptions import ValidationError
from incidents.models import AllocationDecision, Incident
from responders.models import Responder, Load
from django.db.models import F
from scheduler.models import Cycle, IncidentList, DecisionRecord
from django.utils import timezone
from execution.models import Execution, FailureRecord
from responders.selectors import balanced_respons

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
  incidents = Incident.objects.filter(status = 'active').order_by('-prior')
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
    selected_unit = None
    current_avail_obj = None
    reason_text = 'making alloca. auto.'
    avail = Availability.objects.filter(location=incid.location, avail_units__gt=0)
    avail = avail.first()
    if avail:
      total_units = avail.total_units
      avail_units = avail.avail_units
      scarcity_ratio = 0
      if total_units > 0:
        scarcity_ratio = avail_units / total_units
        
      if scarcity_ratio <= 0.25:
        if incid.prior < 40:
          avail = None
      if avail:
        u = Unit.objects.filter(kind=avail.res_kind, location=incid.location)
        u = u.first()
        if u:
          selected_unit = u
          current_avail_obj = avail  
          
    if not selected_unit:
      if priority >= 80:
        stealable_exec = Execution.objects.filter(status__in=['pending', 'started'], incident__prior__lt=40,
          unit__location=incid.location).select_related('incident', 'unit').first()
        if stealable_exec:
          prev_incid = stealable_exec.incident
          selected_unit = stealable_exec.unit  
          stealable_exec.status = 'failed'
          stealable_exec.save()
          FailureRecord.objects.create(execution=stealable_exec, reason=f'high prior {incid.id}')
          reason_text = f'from incid {prev_incid.id}'
    
    if selected_unit is not None:
      respon = balanced_respons()
      respon = respon.first()    
      if not respon:
        continue
      if current_avail_obj:
        current_avail_obj.avail_units -= 1
        current_avail_obj.save()
        
      AllocationDecision.objects.create(incident=incid, unit=selected_unit, allocated_by=None)
      load, _ = Load.objects.get_or_create(responder=respon, incident=incid)
      load.load_count += 1
      load.save()

      decision = DecisionRecord.objects.create(cycle=cycle, incident=incid, unit=selected_unit, responder=respon, reason=reason_text)
      exists = Execution.objects.filter(decision=decision)
      exists = exists.exists()
      if not exists:
        Execution.objects.create(incident=incid, unit=selected_unit, inventory=None, created_by=None, status = 'pending', decision=decision)
      decis_count += 1
    
  cycle.completed_at = timezone.now()
  cycle.total_incids = len(list_data)
  cycle.decis_made = decis_count
  cycle.save()
  return cycle
