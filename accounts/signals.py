from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User, Profile

@receiver(post_save, sender=User)
def user_profile(sender, instance, created, **kwargs):
  if created:
    if instance.is_admin:
      init_cont = 'admin'
    else:
      init_cont = 'citizen'
        
    Profile.objects.create(user=instance, control=init_cont)
  else:
    if hasattr(instance, 'profile'):
      instance.profile.save()