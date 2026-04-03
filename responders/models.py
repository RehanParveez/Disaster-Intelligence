from django.db import models
from accounts.models import User, BaseModel
from resources.models import Unit

class Responder(BaseModel):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'responder_profile')
  skills = models.ManyToManyField('Capability', related_name = 'responders', blank=True)
  max_load = models.PositiveIntegerField(default=3)
    
  def __str__(self):
    return self.user.username

class Capability(BaseModel):
  name = models.CharField(max_length=60)
  description = models.TextField(max_length=70, blank=True, null=True)
   
  def __str__(self):
    return self.name

class Shift(BaseModel):
  responder = models.ForeignKey(Responder, on_delete=models.CASCADE, related_name = 'shifts')
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
    
  class Meta:
    unique_together = ('responder', 'start_time', 'end_time')
    
  def __str__(self):
    return self.responder.user.username

class Load(BaseModel):
  responder = models.ForeignKey(Responder, on_delete=models.CASCADE, related_name = 'loads')
  incident = models.ForeignKey('incidents.Incident', on_delete=models.CASCADE, related_name = 'loads')
  units_assigned = models.ManyToManyField(Unit, related_name = 'responders_assigned', blank=True)
  load_count = models.PositiveIntegerField(default=0) 
    
  class Meta:
    unique_together = ('responder', 'incident')
    
  def __str__(self):
    return self.responder.user.username
