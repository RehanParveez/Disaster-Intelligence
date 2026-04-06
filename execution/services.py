from django.core.exceptions import ValidationError
from execution.models import Execution, ExecutionRecord, FailureRecord
from resources.services import return_unit_serv
from scheduler.tasks import run_sched_cycle
from django.db import transaction
from incidents.models import IncidentPriorRecord
from events.services import make_event

def start_exec(execution_id):
  exec_obj = Execution.objects.get(id=execution_id)
  if exec_obj.status != 'pending':
    raise ValidationError('the exec. should start from pend.')

  exec_obj.status = 'started'
  exec_obj.save()
  ExecutionRecord.objects.create(execution=exec_obj, message = 'the exec. has started')
  return exec_obj

def update_exec(execution_id, message):
  exec_obj = Execution.objects.get(id=execution_id)
  status = exec_obj.status
  if status == 'started':
    pass
  elif status == 'ongoing':
    pass
  else:
    raise ValidationError('the exec. should be start.')

  exec_obj.status = 'ongoing'
  exec_obj.save()
  ExecutionRecord.objects.create(execution=exec_obj, message=message)
  return exec_obj

def complete_exec(execution_id):
  exec_obj = Execution.objects.get(id=execution_id)
  status = exec_obj.status
  if status == 'started':
    pass
  elif status == 'ongoing':
    pass
  else:
    raise ValidationError('the exec, is not active')
  exec_obj.status = 'completed'
  exec_obj.save()
  ExecutionRecord.objects.create(execution=exec_obj, message = 'the exec. is comple.')

  unit = exec_obj.unit
  inventory = exec_obj.inventory
  if not unit:
    return exec_obj
  if not inventory:
    return exec_obj

  return_unit_serv(unit_id=unit.id, inventory_id=inventory.id, user=exec_obj.created_by,
    reason='the exec. is comple.')
  return exec_obj

def fail_exec(execution_id, reason):
  exec_obj = Execution.objects.get(id=execution_id)
  exec_obj.status = 'failed'
  exec_obj.save()
  FailureRecord.objects.create(execution=exec_obj, reason=reason)
  ExecutionRecord.objects.create(execution=exec_obj, message =f'the exec. has failed: {reason}')
  payload = {'execution_id': exec_obj.id, 'reason': reason}
  make_event(kind_name = 'EXECUTION_FAILED', payload=payload)
  
  return exec_obj

@transaction.atomic
def handle_failure(execution):
  incident = execution.incident
  prev_prior = incident.prior
  incident.prior += 10 
  incident.save()

  IncidentPriorRecord.objects.create(incident=incident, prev_prior=prev_prior, new_prior=incident.prior,
    reason = f'due to fail.exec. the auto escal {execution.id}')
  run_sched_cycle.delay()
  return incident

@transaction.atomic
def escalate_incid(incident, reason = 'the manual escal'):
  prev_prior = incident.prior
  incident.prior += 50 
  incident.status = 'verified'
  incident.save()
  IncidentPriorRecord.objects.create(incident=incident, prev_prior=prev_prior, new_prior=incident.prior, reason=reason)
  return incident