# services\posts\management\commands\populate_posts.py

from django.core.management.base import BaseCommand
from faker import Faker
from services.posts.infrastructure.repositories import PostModel


class Command(BaseCommand):
    help = 'Populate the Post table with fake data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=50,
            help='The number of fake posts to create.'
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options['count']

        for _ in range(count):
            title = fake.sentence(nb_words=6)
            content = fake.text(max_nb_chars=200)
            # Create a record using the PostModel Django model
            PostModel.objects.create(
                title=title,
                content=content,
            )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {count} fake posts.'))
