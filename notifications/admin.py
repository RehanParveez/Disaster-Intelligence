from django.contrib import admin
from notifications.models import Notification

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  list_display = ['user', 'message', 'read', 'event_id']
