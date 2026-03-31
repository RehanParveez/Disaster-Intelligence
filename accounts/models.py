from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    abstract = True

class User(AbstractUser, BaseModel):
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=35)
  dob = models.DateField(null=True, blank=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  date_joined = models.DateTimeField(auto_now_add=True)
    
  def __str__(self):
    return self.username

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  location = models.CharField(max_length=55, blank=True, null=True)
  
  def __str__(self):
    return self.user.username


