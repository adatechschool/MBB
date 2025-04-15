# accounts\users\signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User  # adjust the import to your custom user model path
from service.models import (
    Account,
)  # adjust this import if your Account model is in a different location


@receiver(post_save, sender=User)
def create_account_for_new_user(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(
            user_id=instance.pk,
            username=instance.username,
            email=instance.email,
            bio="",  # Optionally, set a default bio
            profile_picture=None,
        )
