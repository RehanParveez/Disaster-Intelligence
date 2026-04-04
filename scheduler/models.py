from django.db import models
from incidents.models import Incident
from resources.models import Unit
from responders.models import Responder

# Create your models here.
class IncidentList(models.Model):
  incident = models.OneToOneField(Incident, on_delete=models.CASCADE, related_name = 'list_entry')
  prior = models.IntegerField()
  position = models.IntegerField()
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.incident.title

class Cycle(models.Model):
  started_at = models.DateTimeField(auto_now_add=True)
  completed_at = models.DateTimeField(null=True, blank=True)
  total_incids = models.IntegerField(default=0)
  decis_made = models.IntegerField(default=0)

  def __str__(self):
    return self.id

class DecisionRecord(models.Model):
  cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name = 'dec_record')
  incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
  unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
  responder = models.ForeignKey(Responder, on_delete=models.SET_NULL, null=True, blank=True)
  reason = models.CharField(max_length=60, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.incident.title
