from django.db import models
from accounts.models import User

class Resource(models.Model):
  name = models.CharField(max_length=55)
  description = models.TextField(max_length=70, blank=True, null=True)

  def __str__(self):
    return self.name

class Unit(models.Model):
  kind = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name = 'units')
  identifier = models.CharField(max_length=70)
  location = models.CharField(max_length=60, blank=True, null=True)
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.kind.name

class Availability(models.Model):
  res_kind = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name = 'availability')
  total_units = models.PositiveIntegerField(default=0)
  avail_units = models.PositiveIntegerField(default=0)
  location = models.CharField(max_length=60)
  last_updated = models.DateTimeField(auto_now=True)

  class Meta:
     unique_together = ('res_kind', 'location')

  def __str__(self):
    return self.res_kind.name