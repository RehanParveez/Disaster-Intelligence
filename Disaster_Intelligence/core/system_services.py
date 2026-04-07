from analytics.models import ResponseRecord, ResourceEfficiency, ResponderPerformance
from incidents.models import Incident
from analytics.services import calc_record
from django.db.models import Count

def recal_all_analy():
  ResponseRecord.objects.all().delete()
  ResourceEfficiency.objects.update(alloca_count=0, failure_count=0)
  ResponderPerformance.objects.update(incid_handl=0, succ_exec=0)

  resolved_incids = Incident.objects.filter(status = 'resolved')
  for incid in resolved_incids:
    calc_record(incid.id)  
  return {'processed_incidents': resolved_incids.count()}

def rebalance_resos():
  critical_unserved = Incident.objects.filter(severity__gte=4, status = 'verified'
  ).annotate(num_allocs=Count('allocations')).filter(num_allocs=0)

  over_served = Incident.objects.filter(severity__lte=2, status = 'verified' 
  ).annotate(num_allocs=Count('allocations')).filter(num_allocs__gt=1)

  suggess = []
  for incid in critical_unserved:
    suggess.append({'incident_id': incid.id, 'title': incid.title, 'alert': 'CRITICAL_GAPS_FOUND',
      'recommendation': 'move the units from low-prior p/t to this incid.'})
      
  return {'critical_gaps': suggess, 'over_served_count': over_served.count()}