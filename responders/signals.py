from django.dispatch import receiver
from django.db.models.signals import post_save
from responders.models import Responder, Load
from analytics.models import ResponderPerformance

@receiver(post_save, sender=Responder)
def responder_perf(sender, instance, created, **kwargs):
  if created:
    ResponderPerformance.objects.get_or_create(responder=instance)
    print(f'the perf record for {instance.user.username}')

@receiver(post_save, sender=Load)
def respond_activity(sender, instance, created, **kwargs):
  if created:
    performance, _ = ResponderPerformance.objects.get_or_create(responder=instance.responder)
    performance.incid_handl += 1
    performance.save()
    print(f'{instance.responder.user.username} is now handl incid {instance.incident.id}')