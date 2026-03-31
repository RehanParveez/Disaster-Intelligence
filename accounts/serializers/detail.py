from rest_framework import serializers
from accounts.models import User, Profile

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'username', 'phone', 'dob', 'is_active', 'is_staff', 'is_admin', 'date_joined', 'created_at', 'updated_at']
  
  def create(self, validated_data):
    user=User.objects.create_user(
    username=validated_data.get('username'),
    email=validated_data.get('email'),
    password=validated_data.get('password'),
    phone=validated_data.get('phone'),
    dob=validated_data.get('dob'),
    is_active=validated_data.get('is_active'),
    is_staff=validated_data.get('is_staff'),
    date_joined=validated_data.get('date_joined'),
    created_at=validated_data.get('created_at'),
    updated_at=validated_data.get('updated_at'),  
    )
    return user

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['user', 'location']