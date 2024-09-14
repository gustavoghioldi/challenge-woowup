from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from email_project.settings import DJANGO_FIRST_PASSWORD


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:

            username = "testuser"
            email = "testuser@admin.com"

            admin = User.objects.create_superuser(
                email=email, username=username, password=DJANGO_FIRST_PASSWORD
            )
            admin.is_active = True
            admin.save()
        else:
            print("Admin accounts can only be initialized if no Accounts exist")
