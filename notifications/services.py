from notifications.models import Notification

def create_notif(user, message, event_id=None):
  notifi = Notification.objects.create(user=user, message=message, event_id=event_id)
  return notifi

def notifi_read(notification_id):
    notifi = Notification.objects.get(id=notification_id)
    notifi.read = True
    notifi.save()
    return notifi