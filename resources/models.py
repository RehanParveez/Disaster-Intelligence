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

class Inventory(models.Model):
  name = models.CharField(max_length=60) 
  location = models.CharField(max_length=60)
  resources = models.ManyToManyField(Unit, related_name = 'inventories')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('name', 'location')

  def __str__(self):
    return self.name

class Consumption(models.Model):
  CHANGE_CHOICES = (
    ('created', 'Created'),
    ('allocated', 'Allocated'),
    ('returned', 'Returned'),
  )
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name = 'records')
  inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'usage_records')
  change_kind = models.CharField(max_length=60, choices=CHANGE_CHOICES, default = 'created')
  prev_avail_units = models.PositiveIntegerField(null=True, blank=True)
  pres_avail_units = models.PositiveIntegerField(null=True, blank=True)
  reason = models.CharField(max_length=70, blank=True, null=True)
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.unit.kind.name
