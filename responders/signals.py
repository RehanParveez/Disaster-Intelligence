from django.dispatch import receiver
from django.db.models.signals import post_save
from responders.models import Responder, Load
from analytics.models import ResponderPerformance
from django.db.models.signals import m2m_changed
from django.core.cache import cache

@receiver(post_save, sender=Responder)
def responder_perf(sender, instance, created, **kwargs):
  if created:
    ResponderPerformance.objects.get_or_create(responder=instance)
    print(f'the perf record for {instance.user.username}')
  cache.clear()

@receiver(post_save, sender=Load)
def respond_activity(sender, instance, created, **kwargs):
  if created:
    performance, _ = ResponderPerformance.objects.get_or_create(responder=instance.responder)
    performance.incid_handl += 1
    performance.save()
    print(f'{instance.responder.user.username} is now handl incid {instance.incident.id}')
    cache.clear()

@receiver(m2m_changed, sender=Responder.skills.through)
def skills_cache(sender, instance, **kwargs):
    cache.clear()
    print(f'the cache is clea. {instance.user.username}')