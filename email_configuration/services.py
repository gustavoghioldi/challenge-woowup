from .models import EmailConfigurationModel
from django.core.cache import cache


class EmailConfigurationService:

    def __get_configuration_in_primary_order() -> dict[dict, str]:
        configurations = EmailConfigurationModel.objects.order_by("-is_primary").values(
            "broker_name", "broker_configuration"
        )
        # Convertir los resultados en un diccionario
        config_dict = {
            config["broker_name"]: config["broker_configuration"]
            for config in configurations
        }
        return config_dict

    @staticmethod
    def get_data():
        cache_key = "email_configuration_cache"
        data = cache.get(cache_key)
        if not data:
            data = EmailConfigurationService.__get_configuration_in_primary_order()
            cache.set(
                cache_key, data, timeout=None
            )  # Cachear indefinidamente hasta que se invalide
        return data
