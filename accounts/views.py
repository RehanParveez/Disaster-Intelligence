from rest_framework import viewsets
from accounts.models import User, Profile
from accounts.serializers.detail import UserSerializer, ProfileSerializer
from Disaster_Intelligence.core.permissions import SelfOnlyPermission

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  permission_classes = [SelfOnlyPermission]
  
  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset
    return self.queryset.filter(id=user.id)

class ProfileViewset(viewsets.ModelViewSet):
  serializer_class = ProfileSerializer
  queryset = Profile.objects.all()
  permission_classes = [SelfOnlyPermission]
  
  def get_queryset(self):
    user = self.request.user
    if user.is_admin:
      return self.queryset
    return self.queryset.filter(user=user)