from django.db import models
from accounts.models import BaseModel
from incidents.models import Incident
from resources.models import Unit, Inventory
from accounts.models import User
from scheduler.models import DecisionRecord

class Execution(BaseModel):
  STATUS_CHOICES = (
    ('started', 'Started'),
    ('pending', 'Pending'),
    ('ongoing', 'OnGoing'),
    ('completed', 'Completed'),
    ('failed', 'Failed')
  )
  incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name = 'executions')
  decision = models.ForeignKey(DecisionRecord, on_delete=models.CASCADE, related_name = 'executions', null=True, blank=True)
  unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
  inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default = 'pending')
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   
class ExecutionRecord(models.Model):
  execution = models.ForeignKey(Execution, on_delete=models.CASCADE, related_name = 'exe_records')
  message = models.CharField(max_length=60)
  updated_at = models.DateTimeField(auto_now_add=True)

class FailureRecord(models.Model):
  execution = models.ForeignKey(Execution, on_delete=models.CASCADE, related_name = 'failures')
  reason = models.CharField(max_length=60)
  updated_at = models.DateTimeField(auto_now_add=True)
