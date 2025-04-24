# posts\service\management\commands\populate_posts.py

"""Populate the posts table with sample data."""

from django.core.management.base import BaseCommand
from common.models import Post, User
from faker import Faker
import random


class Command(BaseCommand):
    help = "Populate the posts table with sample data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of posts to create (default: 100)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        faker = Faker()
        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR(
                "No users found. Please create some users before populating posts."
            ))
            return

        for _ in range(count):
            user = random.choice(users)
            content = faker.paragraph(nb_sentences=5)
            Post.objects.create(user=user, post_content=content)

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {count} posts."
        ))
