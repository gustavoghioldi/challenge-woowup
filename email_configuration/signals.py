from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from .models import EmailConfigurationModel


@receiver(post_save, sender=EmailConfigurationModel)
@receiver(post_delete, sender=EmailConfigurationModel)
def clear_cache(sender, **kwargs):
    if kwargs.get("created") and kwargs.get("instance").is_primary:
        EmailConfigurationModel.objects.filter(is_primary=True).exclude(
            pk=kwargs.get("instance").pk
        ).update(is_primary=False)
    cache.delete_pattern("email_configuration_cache")
