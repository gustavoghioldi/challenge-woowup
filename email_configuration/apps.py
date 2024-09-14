from django.apps import AppConfig


class EmailConfigurationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_configuration"

    def ready(self) -> None:
        import email_configuration.signals

        return super().ready()
