from resources.models import Unit, Inventory, Availability
from rest_framework.exceptions import ValidationError
from incidents.models import AllocationDecision
from responders.models import Responder
from django.db.models import F

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
