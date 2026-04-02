from resources.models import Unit, Availability
from django.core.exceptions import ValidationError

def create_reso(data, user):
  print('the service is working')
  res_kind = data.get('kind')
  identifier = data.get('identifier')
  location = data.get('location')

  if not res_kind:
    raise ValidationError('the res_kind is need.')
  if not identifier:
    raise ValidationError('the identifier is need.')

  reso = Unit.objects.create(kind=res_kind, identifier=identifier, location=location, created_by=user)
  availability, created = Availability.objects.get_or_create(res_kind=res_kind, location=location,
      defaults={'total_units': 1, 'avail_units': 1})
  if not created:
    availability.total_units += 1
    availability.avail_units += 1
    availability.save()
  return reso

def update_avail(resource_id, data):
  reso = Unit.objects.get(id=resource_id)
  avail = Availability.objects.get(res_kind=reso.kind, location=reso.location)

  pres_avail = data.get('avail_units')
  if pres_avail is None:
    raise ValidationError('the avail_units are need.')
  if pres_avail > avail.total_units:
    raise ValidationError('the avail units cant be > total units')

  avail.avail_units = pres_avail
  avail.save()
  return avail