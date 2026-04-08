from django.dispatch import receiver
from django.db.models.signals import post_save
from events.models import Event
from events.services import process_event

@receiver(post_save, sender=Event)
def event_process(sender, instance, created, **kwargs):
  if created:
    if not instance.is_processed:
      process_event(instance.id)
      print(f'the event {instance.event_kind.name} is process.')