from events.models import EventKind, Event, EventRecord
from django.db import transaction
from execution.models import Execution
from scheduler.tasks import run_sched_cycle
from incidents.models import Incident

def make_event(kind_name, payload):
  kind, _ = EventKind.objects.get_or_create(name=kind_name)
  event = Event.objects.create(event_kind=kind, payload=payload) 
  process_event(event.id)
  return event

@transaction.atomic
def process_event(event_id):
    event = Event.objects.get(id=event_id)
    kind = event.event_kind.name
    data = event.payload
    was_successful = False

    if kind == 'EXECUTION_FAILED':
      exec_obj = Execution.objects.get(id=data['execution_id'])
      from execution.services import handle_failure, escalate_incid  ## passed here due to circular import issue
      handle_failure(exec_obj)
      run_sched_cycle.delay()
      EventRecord.objects.create(event=event, status = 'success', message = f'handl. failure for the exec. {exec_obj.id}')
      was_successful = True

    elif kind == 'INCIDENT_ESCALATED':
      incid_obj = Incident.objects.get(id=data['incident_id'])
      reason = data.get('reason', 'Manual Escalation')
        
      escalate_incid(incid_obj, reason=reason)
      EventRecord.objects.create(event=event, status = 'success', message = f'the  incid. is escal {incid_obj.id}')
      was_successful = True
    
    if was_successful:
      event.is_processed = True
      event.save()
    return event