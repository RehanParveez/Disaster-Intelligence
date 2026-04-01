from django.db import models
from accounts.models import User

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
