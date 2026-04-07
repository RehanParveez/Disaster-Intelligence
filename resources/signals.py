from django.dispatch import receiver
from django.db.models.signals import post_save
from resources.models import Unit, Consumption
from analytics.models import ResourceEfficiency

@receiver(post_save, sender=Unit)
def unit_effic(sender, instance, created, **kwargs):
  if created:
    ResourceEfficiency.objects.get_or_create(unit=instance, reso_kind=instance.kind)
    print(f'the effic rec {instance.identifier}')

@receiver(post_save, sender=Consumption)
def effic_stats(sender, instance, created, **kwargs):
  if created:
    if instance.change_kind == 'allocated':     
      efficiency, _ = ResourceEfficiency.objects.get_or_create(unit=instance.unit, reso_kind=instance.unit.kind) 
      efficiency.alloca_count += 1
      efficiency.save()
      print(f'the upd count for alloc {instance.unit.identifier}')