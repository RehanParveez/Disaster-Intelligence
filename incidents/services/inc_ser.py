from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from incidents.models import Incident, IncidentReport, IncidentGroup, IncidentPriorRecord
from incidents.selectors.inc_sel import nearby_inc, inc_id, group_by_loc
from incidents.models import AllocationDecision
from resources.services import return_unit_serv
from django.utils import timezone
import datetime

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
  IncidentReport.objects.create(incident=incid, reported_by=user, description=description, location=location)
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

def group_incid(incident_id):
  incid = Incident.objects.get(id=incident_id)
  if incid.group:
    return incid.group
  group = group_by_loc(incid.location)

  if group:
    incid.group = group
    incid.save()
    group.group_size += 1
    group.save()
    return group
  else:
    group = IncidentGroup.objects.create(location=incid.location, group_size=1)
    incid.group = group
    incid.save()
    return group

def cal_prior(incident_id, reason = 'auto re-eval'):
  incid = Incident.objects.get(id=incident_id)
  prev_prior = incid.prior
  severity = incid.severity * 10
  rep_count = incid.reports.count() * 2
  
  wait_mins = (timezone.now() - incid.created_at).total_seconds() / 60
  wait_score = (wait_mins // 10) * 5
  
  multiplier = 1.0
  criti_events = ['flood', 'explosion', 'earthquake', 'death', 'fire']
  criti_locs = ['hospital', 'school', 'bridge', 'plant', 'refinery']
  
  title = incid.title.lower()
  critical_event = False
  for word in criti_events:
    if word in title:
      critical_event = True
      break
    
  location = incid.location.lower()
  critical_location = False
  for word in criti_locs:
    if word in location:
      critical_location = True
      break
    
  multiplier = 1.0
  if critical_event:
    if critical_location:
      multiplier = 2.0
    else:
      multiplier = 1.5
  else:
    if critical_location:
      multiplier = 1.5
    
  new_prior = int((severity + rep_count + wait_score) * multiplier)
  if prev_prior != new_prior:
    incid.prior = new_prior
    incid.save()
    IncidentPriorRecord.objects.create(incident=incid, prev_prior=prev_prior, new_prior=new_prior, reason=reason)
  return incid

@transaction.atomic
def return_unit_delete(incident, unit_id, user, reason=None):
  alloca = AllocationDecision.objects.filter(unit_id=unit_id, incident=incident)
  alloca = alloca.first()
  if not alloca:
    raise ValidationError('the unit is not alloca to this incid')
  return_unit_serv(unit_id=unit_id, inventory_id=alloca.inventory_id, user=user, reason=reason)
  alloca.delete()
  return True
  