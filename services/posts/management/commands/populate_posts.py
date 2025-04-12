# services\posts\management\commands\populate_posts.py

from django.core.management.base import BaseCommand
from faker import Faker
from services.posts.domain.models import PostModel
from services.roles.domain.models import RoleModel
from services.users.domain.models import UserModel

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

        # Ensure a default role exists (using RoleModel.USER as the default role)
        default_role, _ = RoleModel.objects.get_or_create(
            role_name=RoleModel.USER,
            defaults={'role_name': RoleModel.USER}
        )

        # Get or create a default user with the default role
        default_user, user_created = UserModel.objects.get_or_create(
            username='default',
            defaults={
                'email': 'default@example.com',
                'role': default_role,
            }
        )
        if user_created:
            # Set a password if created
            default_user.set_password('defaultpassword')
            default_user.save()

        for _ in range(count):
            title = fake.sentence(nb_words=6)
            content = fake.text(max_nb_chars=200)
            # Create a record using the PostModel Django model with a user
            PostModel.objects.create(
                title=title,
                content=content,
                user=default_user,
            )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {count} fake posts.'
        ))
