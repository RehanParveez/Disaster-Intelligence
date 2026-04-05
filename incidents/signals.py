from django.db.models.signals import post_save
from django.dispatch import receiver
from incidents.models import IncidentReport, Incident
from incidents.services.inc_ser import group_incid, cal_prior
from scheduler.tasks import run_sched_cycle

@receiver(post_save, sender=IncidentReport)
def incid_report(sender, instance, created, **kwargs):
  if not created:
    return
  incident = instance.incident
  group_incid(incident.id)
  cal_prior(incident.id)
  run_sched_cycle.delay()
  
@receiver(post_save, sender=Incident)
def incid_creation(sender, instance, created, **kwargs):
  if not created:
    return 
  group_incid(instance.id)