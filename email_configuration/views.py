from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import EmailConfigurationSerializer
from .models import EmailConfigurationModel


class EmailConfigurationListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailConfigurationSerializer
    queryset = EmailConfigurationModel.objects.all()


class EmailConfigurationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailConfigurationSerializer
    queryset = EmailConfigurationModel.objects.all()

    def perform_update(self, serializer):
        if (
            not (serializer.validated_data.get("is_primary"))
            and EmailConfigurationModel.objects.filter(
                is_primary=True, broker_name=self.kwargs.get("pk")
            ).exists()
        ):
            raise ValidationError(
                {
                    "message": f'{self.kwargs.get("pk")} is primary, first change to other service the primary'
                }
            )
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.is_primary:
            raise ValidationError(
                {
                    "message": f"{instance.broker_name} is primary, first change to other service the primary"
                }
            )
        return super().perform_destroy(instance)
