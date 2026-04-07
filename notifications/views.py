from rest_framework import viewsets
from notifications.serializers import NotificationSerializer
from rest_framework.decorators import action
from notifications.models import Notification
from rest_framework.response import Response
from notifications.services import notifi_read
from Disaster_Intelligence.core.permissions import SelfOnlyPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class NotificationViewset(viewsets.ReadOnlyModelViewSet):
  serializer_class = NotificationSerializer
  queryset = Notification.objects.all()
  permission_classes = [SelfOnlyPermission]
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  
  # filtering fields
  search_fields = ['message']
  ordering_fields = ['created_at']
  filterset_fields = ['read', 'event_id', 'created_at']
    
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)

  @action(detail=True, methods=['post'])
  def read(self, request, pk=None):
    notifi_read(pk)
    return Response({'message': 'the notifi is read'}, status=200)
