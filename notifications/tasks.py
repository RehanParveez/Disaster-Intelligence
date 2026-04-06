from celery import shared_task
from django.contrib.auth import get_user_model
from notifications.models import Notification
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_notification(user_id, message, event_id=None):
  User = get_user_model()
  user = User.objects.get(id=user_id)
  Notification.objects.create(user=user, message=message, event_id=event_id)
  send_mail(
    subject = 'the disaster alert',
    message=message,
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[user.email],
    fail_silently=False
  )
  return f'the notif. is sent to {user.username}'