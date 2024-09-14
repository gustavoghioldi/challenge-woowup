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

    def __send_my_email(
        self,
        subject: str,
        message: str,
        from_email: str,
        recipient_list: list[str],
        attempt: int,
    ) -> None:
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

    def sending(self, subject, message, from_email, recipient_list) -> list:
        max_attempts = len(self.backends)
        if max_attempts == 0:
            return {
                "error": "There are no services available, you must add at least one. see: https://2trdeh54hp.apidog.io/api-10084794"
            }, status.HTTP_424_FAILED_DEPENDENCY

        for attempt in range(max_attempts):
            try:
                self.__send_my_email(
                    subject, message, from_email, recipient_list, attempt
                )
                return {
                    "message": f"Emails sent successfully with {self.backends[attempt]}"
                }, status.HTTP_200_OK
            except AnymailAPIError as e:

                logger.error(f"Intento {attempt + 1} fallido: {str(e)}")
                if attempt + 1 == max_attempts:
                    return {
                        "error": "Cannot establish connection with any messaging service"
                    }, status.HTTP_424_FAILED_DEPENDENCY
