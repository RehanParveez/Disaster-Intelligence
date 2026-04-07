from django.db import models
from accounts.models import User, BaseModel
from incidents.models import Incident
from resources.models import Unit, Resource
from responders.models import Responder

class ResponseRecord(BaseModel):
  incident = models.OneToOneField(Incident, on_delete=models.CASCADE, related_name = 'analytics_record')
  disp_time_sec = models.PositiveIntegerField(default=0)
  total_reso_time = models.PositiveIntegerField(default=0)
  primary_auth = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'decisions_record')

  class Meta:
    ordering = ['-created_at']
    
  def __str__(self):
    return f'{self.incident.title}'

class ResourceEfficiency(BaseModel):
  reso_kind = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name = 'efficiency_stats')
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name = 'unit_record')
  alloca_count = models.PositiveIntegerField(default=0)
  failure_count = models.PositiveIntegerField(default=0)
  active_hours = models.FloatField(default=0.0)

  class Meta:
    ordering = ['-created_at']
    
  def __str__(self):
    return f'{self.reso_kind.name}'

class ResponderPerformance(BaseModel):
  responder = models.ForeignKey(Responder, on_delete=models.CASCADE, related_name = 'performance')
  incid_handl = models.PositiveIntegerField(default=0)
  avg_peak_load = models.FloatField(default=0.0)
  succ_exec = models.PositiveIntegerField(default=0)
  
  class Meta:
    ordering = ['-created_at']
          
  def __str__(self):
    return f'{self.responder.user.username}'