from django.dispatch import receiver
from django.db.models.signals import post_save
from incidents.models import Incident
from .services import calc_record
from django.core.cache import cache

@receiver(post_save, sender=Incident)
def calc_analy(sender, instance, created, **kwargs):
  if not created:
    if instance.status == 'resolved':
      calc_record(instance.id)
      print(f'the analy for incid: {instance.title}')
      
@receiver(post_save, sender=Incident)
def analy_cache(sender, instance, **kwargs):
  new = kwargs.get('created')
  if new:
    return  
  if instance.status == 'resolved':
    cache.delete('system_rebalance_data')
    cache.clear()  
    print(f'sign. cleared for {instance.title}')
    