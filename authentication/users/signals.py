# accounts\users\signals.py

"""Signal handlers for creating associated accounts when new users are created."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User  # adjust the import to your custom user model path
from service.models import (
    Account,
)  # adjust this import if your Account model is in a different location


@receiver(post_save, sender=User)
def create_account_for_new_user(_, instance, created, **kwargs):
    """Create an associated Account instance when a new User is created.

    Args:
        sender: The model class that sent the signal
        instance: The actual instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if created:
        Account.objects.create(
            user_id=instance.pk,
            username=instance.username,
            email=instance.email,
            bio="",  # Optionally, set a default bio
            profile_picture=None,
        )
