from django.db import transaction
from django.core.exceptions import ValidationError
from responders.models import Responder, Capability, Shift
from django.core.cache import cache

@transaction.atomic
def register_respon(user, data):
  if hasattr(user, 'responder_profile'):
    raise ValidationError('the user is already a respon')

  max_load = data.get('max_load', 3)
  skills_ids = data.get('skills', [])
  respon = Responder.objects.create(user=user, max_load=max_load)
  
  capabilities = Capability.objects.filter(id__in=skills_ids)
  if skills_ids:
    if not capabilities.exists():
      raise ValidationError('the skills are wrong')
  respon.skills.set(capabilities)
  return respon

@transaction.atomic
def set_avail(responder_id, schedule):
  respon = Responder.objects.filter(id=responder_id)
  respon = respon.first()
  if not respon:
    raise ValidationError('the respon is not pres.')
  start_time = schedule.get('start_time')
  end_time = schedule.get('end_time')

  if not start_time:
    raise ValidationError('the start time is need.')
  if not end_time:
    raise ValidationError('the end time is need.')
  if start_time >= end_time:
    raise ValidationError('the shift time is wrong')

  cover = Shift.objects.filter(responder=respon, start_time__lt=end_time, end_time__gt=start_time)
  cover = cover.exists()
  if cover:
    raise ValidationError('the shift covers the pres. schedule')
  shift = Shift.objects.create(responder=respon, start_time=start_time, end_time=end_time)
  cache.clear()
  return shift