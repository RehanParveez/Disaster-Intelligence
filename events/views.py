from rest_framework import viewsets
from events.serializers.detail import EventSerializer, EventRecordSerializer
from events.models import Event
from rest_framework.decorators import action
from events.services import process_event
from rest_framework.response import Response
from Disaster_Intelligence.core.permissions import RoleBasedPermission

class EventViewset(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [RoleBasedPermission]
    allowed_roles = ['admin', 'authority']
    
    def get_queryset(self):
      user = self.request.user
      if user.is_admin:
        return self.queryset
      user_role = getattr(user.profile, 'control', None)
      if user_role == 'authority':
        return self.queryset
      return self.queryset.none()
  
    def perform_create(self, serializer):
      event = serializer.save()
      process_event(event.id)
    
    @action(detail=True, methods=['post'])
    def replay(self, request, pk=None):
      event = self.get_object()
      proces_event = process_event(event.id)
        
      return Response({'message': f'the event {pk} is repla.', 'is_processed': proces_event.is_processed,
        'kind': proces_event.event_kind.name}, status=200)

    @action(detail=True, methods=['get'])
    def event_rec(self, request, pk=None):
      event = self.get_object()
      records = event.event_records.all()
      serializer = EventRecordSerializer(records, many=True)
      return Response(serializer.data)