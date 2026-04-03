from django.db import models
from accounts.models import User, BaseModel
from resources.models import Unit, Inventory
from responders.models import Responder, Load

# Create your models here.
class Incident(models.Model):
  STATUS_CHOICES = (
    ('active', 'Active'),
    ('verified', 'Verified'),
    ('rejected', 'Rejected'),
   )
  title = models.CharField(max_length=60)
  description = models.TextField()
  location = models.CharField(max_length=55)
  severity = models.IntegerField()
  prior = models.IntegerField(default=0)
  group = models.ForeignKey('IncidentGroup', on_delete=models.SET_NULL, null=True, blank=True, related_name = 'incidents')
  assigned_responders = models.ManyToManyField(Responder, through=Load, related_name = 'incidents_assigned', blank=True)
  status = models.CharField(max_length=55, choices=STATUS_CHOICES, default = 'active')
  created_by = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.title
  
class IncidentReport(models.Model):
  incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name = 'reports')
  reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
  description = models.TextField()
  location = models.CharField(max_length=55)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.location

class IncidentGroup(BaseModel):
  location = models.CharField(max_length=60)
  group_size = models.IntegerField(default=0)
  
  def __str__(self):
    return self.location

class IncidentPriorRecord(models.Model):
  incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name = 'prior_record')
  prev_prior= models.IntegerField()
  new_prior = models.IntegerField()
  reason = models.CharField(max_length=60)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.incident.title

class AllocationDecision(models.Model):
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name = 'allocations')
  incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name = 'allocations')
  allocated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'allocations_done')
  inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'allocations')
  reason = models.CharField(max_length=70, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together = ('unit', 'incident') 
  
  def __str__(self):
    return self.incident.title