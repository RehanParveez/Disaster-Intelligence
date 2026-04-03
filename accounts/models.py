from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    abstract = True

CONTROL_CHOICES = (
  ('citizen', 'Citizen'),
  ('responder', 'Responder'),
  ('admin', 'Admin'),
  ('authority', 'Authority'),
 )

class User(AbstractUser, BaseModel):
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=35)
  dob = models.DateField(null=True, blank=True)
  is_admin = models.BooleanField(default=False)
    
  def __str__(self):
    return self.username

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  control = models.CharField(max_length=50, choices=CONTROL_CHOICES, default = 'citizen')
  location = models.CharField(max_length=55, blank=True, null=True)
  
  def __str__(self):
    return self.user.username


