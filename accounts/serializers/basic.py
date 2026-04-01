from rest_framework import serializers
from accounts.models import User, Profile

class UserSerializer1(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'password', 'username']
    
class ProfileSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['user']