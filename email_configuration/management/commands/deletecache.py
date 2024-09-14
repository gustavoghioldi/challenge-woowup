from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("cleaning cache... ")
        cache.delete_pattern("email_configuration_cache")
