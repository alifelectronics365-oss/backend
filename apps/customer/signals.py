from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from apps.customer.models.profile_info import ProfileInfo   # adjust import if needed


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create ProfileInfo only for new users
        ProfileInfo.objects.get_or_create(user=instance)
