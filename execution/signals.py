from django.dispatch import receiver
from django.db.models.signals import post_save
from execution.models import Execution
from execution.services import handle_failure
from analytics.services import calc_record

@receiver(post_save, sender=Execution)
def exec_results(sender, instance, created, **kwargs):
  if instance.status == 'failed':
    handle_failure(instance)
    print(f'incid failure {instance.incident.id} is escal.')
  if instance.status == 'completed':
    incident = instance.incident
        
    total_exe = incident.executions.count()
    completed_exe = incident.executions.filter(status = 'completed').count()
        
    if total_exe == completed_exe:
      incident.status = 'resolved'
      incident.save()   
      calc_record(incident.id)
      print(f'the incid {incident.id} is resol.')