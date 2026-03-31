from rest_framework import viewsets
from accounts.models import User, Profile
from accounts.serializers.detail import UserSerializer, ProfileSerializer

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()

class ProfileViewset(viewsets.ModelViewSet):
  serializer_class = ProfileSerializer
  queryset = Profile.objects.all()