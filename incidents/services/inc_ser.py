from django.db import transaction
from django.core.exceptions import PermissionDenied
from incidents.models import Incident, IncidentReport
from incidents.selectors.inc_sel import nearby_inc, inc_id

@transaction.atomic
def inc_report(data, user):
  location = data.get('location')
  description = data.get('description')
  severity = data.get('severity')
  title = data.get('title')
  
  if not location:
    raise ValueError('loca is required')
  if not description:
    raise ValueError('desc is required')

  incid = nearby_inc(location)
  if incid is None:
    incid = Incident.objects.create(title=title, description=description, location=location, severity=severity,
      created_by=user, status = 'active')
  report = IncidentReport.objects.create(incident=incid, reported_by=user, description=description, location=location)
  return incid

def verifiy_inc(incident_id, user):
  incid = inc_id(incident_id)
  if not user.is_admin:
    raise PermissionDenied('the admin can verify only')
  incid.status = 'verified'
  incid.save()
  return incid

def reject_inc(incident_id, user):
  incid = inc_id(incident_id)
  if not user.is_admin:
    raise PermissionDenied('the admin can reject only')
  incid.status = 'rejected'
  incid.save()
  return incid
  