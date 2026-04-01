from incidents.models import Incident

def inc_id(incident_id):
  return Incident.objects.get(id=incident_id)

def all_inc():
  return Incident.objects.all()

def nearby_inc(location):
  inc = Incident.objects.filter(location=location, status = 'active')
  inc = inc.first()
  return inc