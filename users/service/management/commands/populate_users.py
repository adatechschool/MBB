# users\service\management\commands\populate_users.py

"""Populate users with test data."""

from django.core.management.base import BaseCommand
from faker import Faker
from common.models import User, Role


class Command(BaseCommand):
    help = "Populate the database with fake users for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=20,
            help='Number of fake users to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker()
        role, _ = Role.objects.get_or_create(role_name='user')
        for _ in range(count):
            username = fake.user_name()
            email = fake.unique.email()
            user = User(username=username, email=email, role=role)
            user.set_password('password123')
            user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} fake users")
        )
