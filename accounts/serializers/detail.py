from rest_framework import serializers
from accounts.models import User, Profile
from accounts.serializers.basic import ProfileSerializer1

class UserSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer1(read_only=True)
  class Meta:
    model = User
    fields = ['email', 'username', 'password', 'profile', 'phone', 'dob', 'is_admin']
    extra_kwargs = {'password': {'write_only': True}}
  
  def create(self, validated_data):
    user=User.objects.create_user(
    username=validated_data.get('username'),
    email=validated_data.get('email'),
    password=validated_data.get('password'),
    phone=validated_data.get('phone'),
    dob=validated_data.get('dob'),
    )
    return user

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['user', 'location']