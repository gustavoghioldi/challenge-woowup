import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import EmailSerializer
from .service import HandleEmailService

logger = logging.getLogger(__name__)


class SendEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subject = serializer.validated_data["subject"]
        message = serializer.validated_data["message"]
        from_email = serializer.validated_data["from_email"]
        recipient_list = serializer.validated_data["recipient_list"]
        handle_email_service = HandleEmailService()
        json_response, status_code = handle_email_service.sending(
            subject, message, from_email, recipient_list
        )
        return Response(json_response, status=status_code)
