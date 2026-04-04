from celery import shared_task
from scheduler.services import run_cycle
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def run_sched_cycle():
  cycle = run_cycle()
  send_mail(
    subject=f'the sched. cycle {cycle.id}',
    message=f'the cycle {cycle.id} has comple.',
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[settings.EMAIL_HOST_USER],
    fail_silently=False
   )
  return cycle.id