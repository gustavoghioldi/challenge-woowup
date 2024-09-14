from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True, max_length=255)
    message = serializers.CharField(required=True)
    from_email = serializers.EmailField(required=True)
    recipient_list = serializers.ListField(
        required=True, child=serializers.EmailField()
    )
