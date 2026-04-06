from django.db import models
from accounts.models import BaseModel

class EventKind(models.Model):
 name = models.CharField(max_length=70, unique=True) 
 description = models.TextField(blank=True)

 def __str__(self):
    return self.name

class Event(BaseModel):
  event_kind = models.ForeignKey(EventKind, on_delete=models.PROTECT, related_name = 'events')
  payload = models.JSONField()
  is_processed = models.BooleanField(default=False)

  def __str__(self):
    return self.event_kind.name

class EventRecord(models.Model):
  STATUS_CHOICES = (
    ('success', 'Success'),
    ('failed', 'Failed'),
    ('pending', 'Pending'),
  )
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name = 'event_records')
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default = 'pending')
  message = models.CharField(max_length=60)
  processed_at = models.DateTimeField(auto_now_add=True)
