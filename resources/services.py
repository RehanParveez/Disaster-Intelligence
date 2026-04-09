from resources.models import Resource, Unit, Availability, Consumption, Inventory
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from incidents.models import Incident

def create_unit(data, user):
  print('the service is working')
  res_kind = data.get('kind')
  res_kind = Resource.objects.filter(id=res_kind)
  res_kind = res_kind.first()
  if not res_kind:
    raise ValidationError('the reso kind is not pres.')
  identifier = data.get('identifier')
  location = data.get('location')

  if not res_kind:
    raise ValidationError('the res_kind is need.')
  if not identifier:
    raise ValidationError('the identifier is need.')

  unit = Unit.objects.create(kind=res_kind, identifier=identifier, location=location, created_by=user)
  availability, created = Availability.objects.get_or_create(res_kind=res_kind, location=location,
      defaults={'total_units': 1, 'avail_units': 1})
  if not created:
    availability.total_units += 1
    availability.avail_units += 1
    availability.save()
  
  Consumption.objects.create(unit=unit, inventory=None, change_kind = 'created', prev_avail_units=None,
    pres_avail_units=1, created_by=user, reason = 'the unit is created')
  return unit

def allocate_unit_serv(unit_id, inventory_id, user, incident_id, reason=None):
  unit = Unit.objects.filter(id=unit_id)
  unit = unit.first()
  if not unit:
    raise ValidationError('the unit is not pres.')
  invent = Inventory.objects.filter(id=inventory_id)
  invent = invent.first()
  if not invent:
    raise ValidationError('the invent. is not pres.')
  avail = Availability.objects.filter(res_kind=unit.kind, location=unit.location)
  avail = avail.first()
  if not avail:
    raise ValidationError('the avail. is not pres.')
  
  incid = Incident.objects.filter(id=incident_id)
  incid = incid.first()
  if not incid:
    raise ValidationError('the incid is not pres.')
  total_units = avail.total_units
  avail_units = avail.avail_units

  scarcity_ratio = 0
  if total_units > 0:
    scarcity_ratio = avail_units / total_units
  low_stock = False
  if scarcity_ratio <= 0.25:
    low_stock = True
  
  low_priority = False
  if incid.prior < 40:
    low_priority = True
  if low_stock:
    if low_priority:
      raise ValidationError(f'{int(scarcity_ratio * 100)}% of {unit.kind.name} is rem.'
        f'cant alloc to incid with prior. {incid.prior}. its for high prior (>40).')
  
  if avail.avail_units <= 0:
    raise ValidationError('no unit is avail.')
  
  prev_units = avail.avail_units
  avail.avail_units -= 1
  avail.save()
  invent.resources.add(unit)
  
  Consumption.objects.create(unit=unit, inventory=invent, change_kind = 'allocated', prev_avail_units=prev_units,
    pres_avail_units=avail.avail_units, created_by=user, reason=reason)
  cache.clear()
  return avail

def return_unit_serv(unit_id, inventory_id, user, reason=None):
    unit = Unit.objects.filter(id=unit_id)
    unit = unit.first()
    if not unit:
      raise ValidationError('the unit is not pres.')
    invent = Inventory.objects.filter(id=inventory_id)
    invent = invent.first()
    if not invent:
      raise ValidationError('the invent is not pres.')
    avail = Availability.objects.filter(res_kind=unit.kind, location=unit.location)
    avail = avail.first()
    if not avail:
      raise ValidationError('the avail is not pres.')
  
    prev_units = avail.avail_units
    avail.avail_units += 1
    avail.save()
    invent.resources.remove(unit)

    Consumption.objects.create(unit=unit, inventory=invent, change_kind = 'returned', prev_avail_units=prev_units,
      pres_avail_units=avail.avail_units, created_by=user, reason=reason)
    return avail
  
def update_avail(resource_id, data):
  reso = Unit.objects.get(id=resource_id)
  avail = Availability.objects.get(res_kind=reso.kind, location=reso.location)

  pres_avail = data.get('avail_units')
  if pres_avail is None:
    raise ValidationError('the avail_units are need.')
  if not str(pres_avail).isdigit():
    raise ValidationError('the avail_units should be a num.')
  pres_avail = int(pres_avail)
  if pres_avail > avail.total_units:
    raise ValidationError('the avail units cant be > total units')

  avail.avail_units = pres_avail
  avail.save()
  cache.clear()
  return avail