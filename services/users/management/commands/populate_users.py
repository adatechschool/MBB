from django.core.management.base import BaseCommand
from faker import Faker
from services.users.domain.models import UserModel


class Command(BaseCommand):
    help = "Populate the database with fake users."

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(10):
            user = UserModel(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))