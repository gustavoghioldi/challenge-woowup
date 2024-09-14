from django.db import models
from django.core.exceptions import ValidationError


class EmailConfigurationModel(models.Model):
    broker_name = models.CharField(max_length=255, primary_key=True)
    broker_configuration = models.JSONField()
    is_primary = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.is_primary:
    #         self._deactivate_other_primaries()

    # def _deactivate_other_primaries(self):
    #     EmailConfigurationModel.objects.filter(is_primary=True).exclude(
    #         pk=self.pk
    #     ).update(is_primary=False)
    #     if not EmailConfigurationModel.objects.filter(is_primary=True).exists():
    #         self.is_primary = True
    #         super().save(update_fields=["is_primary"])
