from rest_framework import serializers
from .models import EmailConfigurationModel


class EmailConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfigurationModel
        fields = "__all__"
