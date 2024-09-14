import logging
from anymail.message import AnymailMessage
from anymail.exceptions import AnymailAPIError
from django.core.mail import get_connection
from rest_framework import status
from email_configuration.services import EmailConfigurationService

logger = logging.getLogger(__name__)


class HandleEmailService:
    def __init__(self):
        self.configuration_in_primary_order = EmailConfigurationService.get_data()
        self.backends = list(self.configuration_in_primary_order.keys())

    def __get_email_backend(self, attempt):
        backend_path = self.configuration_in_primary_order[
            self.backends[attempt % len(self.backends)]
        ]
        return get_connection(**backend_path)

    def __send_my_email(self, subject, message, from_email, recipient_list, attempt):
        backend = self.__get_email_backend(attempt)
        email = AnymailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[from_email],
            bcc=recipient_list,
            connection=backend,
        )
        email.attach_alternative(message, "text/html")
        email.send()

    def sending(self, subject, message, from_email, recipient_list):
        max_attempts = len(self.backends)
        for attempt in range(max_attempts):
            try:
                self.__send_my_email(
                    subject, message, from_email, recipient_list, attempt
                )
                return {"message": "Emails sent successfully"}, status.HTTP_200_OK
            except AnymailAPIError as e:
                logger.error(f"Intento {attempt + 1} fallido: {str(e)}")
                if attempt + 1 == max_attempts:
                    return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
