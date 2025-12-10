from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.customer.models import User
from apps.notify.models.welcome import Welcome


@receiver(post_save, sender=User)
def create_welcome_notification(sender, instance, created, **kwargs):
    if created:
        Welcome.objects.create(user=instance)
