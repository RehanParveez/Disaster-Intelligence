from django.db import models
from accounts.models import BaseModel
from accounts.models import User

class Notification(BaseModel):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'notifications')
  message = models.CharField(max_length=60)
  read = models.BooleanField(default=False)
  event_id = models.IntegerField(null=True, blank=True) 

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f'{self.user.username}'
