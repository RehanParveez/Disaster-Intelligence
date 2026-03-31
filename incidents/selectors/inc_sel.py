from incidents.models import Incident

def inc_id(incident_id):
  return Incident.objects.get(id=incident_id)

def all_inc():
  return Incident.objects.all()

def filter_inc(location=None, severity=None, status=None):
  inc = Incident.objects.all()
  if location:
    inc = inc.filter(location=location)
  if severity:
    inc = inc.filter(severity=severity)
  if status:
    inc = inc.filter(status=status)
  return inc

def nearby_inc(location):
  inc = Incident.objects.filter(location=location, status = 'active')
  inc = inc.first()
  return inc