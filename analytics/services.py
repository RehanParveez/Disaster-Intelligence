from incidents.models import Incident, AllocationDecision
from django.utils import timezone
from analytics.models import ResponseRecord, ResponderPerformance, ResourceEfficiency
from execution.models import Execution

def calc_record(incident_id):
  incident = Incident.objects.get(id=incident_id)
  first_alloc = AllocationDecision.objects.filter(incident=incident).order_by('created_at')
  first_alloc = first_alloc.first()
    
  disp_time = 0
  if first_alloc:
    disp_time = (first_alloc.created_at - incident.created_at)
    disp_time = disp_time.total_seconds()
    
  total_time = (timezone.now() - incident.created_at)
  total_time = total_time.total_seconds()
    
  disp_time_sec = int(disp_time)
  total_reso_time = int(total_time)
  primary_auth = None

  if first_alloc:
    primary_auth = first_alloc.allocated_by
    defs_data = {'disp_time_sec': disp_time_sec, 'total_reso_time': total_reso_time,
      'primary_auth': primary_auth}
    ResponseRecord.objects.update_or_create(incident=incident, defaults=defs_data)

  for responder in incident.assigned_responders.all():
    perf, _ = ResponderPerformance.objects.get_or_create(responder=responder)
    success_count = Execution.objects.filter(incident=incident, status = 'success').count()
    perf.succ_exec += success_count
    perf.save()

  for alloc in incident.allocations.all():
    eff, _ = ResourceEfficiency.objects.get_or_create(unit=alloc.unit, reso_kind=alloc.unit.kind)
    if Execution.objects.filter(incident=incident, status = 'failed').exists():
      eff.failure_count += 1
    eff.save()