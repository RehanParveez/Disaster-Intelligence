from django.contrib import admin
from events.models import EventKind, Event, EventRecord

# Register your models here.
@admin.register(EventKind)
class EventKindAdmin(admin.ModelAdmin):
  list_display = ['name', 'description']
  
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  list_display = ['event_kind', 'payload', 'is_processed']
  
@admin.register(EventRecord)
class EventRecordAdmin(admin.ModelAdmin):
  list_display = ['event', 'status', 'message', 'processed_at']
