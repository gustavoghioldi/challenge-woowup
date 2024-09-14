from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from anymail.exceptions import AnymailAPIError
from .serializers import EmailSerializer


class EmailSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            "subject": "Test Subject",
            "message": "Test Message",
            "from_email": "test@example.com",
            "recipient_list": ["recipient1@example.com", "recipient2@example.com"],
        }
        serializer = EmailSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            "subject": "",
            "message": "Test Message",
            "from_email": "invalid-email",
            "recipient_list": ["recipient1@example.com", "recipient2@example.com"],
        }
        serializer = EmailSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class JWTAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()

    def test_jwt_authentication(self):
        response = self.client.post(
            "/api/token/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class SendEmailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    @patch("anymail.message.AnymailMessage.send")
    def test_send_email_success(self, mock_send_mail):
        mock_send_mail.return_value = 1  # Simula que el correo fue enviado exitosamente
        data = {
            "subject": "Test Subject",
            "message": "Test Message",
            "from_email": "test@example.com",
            "recipient_list": ["recipient1@example.com", "recipient2@example.com"],
        }
        response = self.client.post("/api/send-email/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Emails sent successfully")

    @patch("anymail.message.AnymailMessage.send")
    def test_send_email_failover(self, mock_send_mail):
        mock_send_mail.side_effect = [
            AnymailAPIError("Primary failed"),
            1,
        ]  # Simula fallo del broker primario y éxito en de secundario
        data = {
            "subject": "Test Subject",
            "message": "Test Message",
            "from_email": "test@example.com",
            "recipient_list": ["recipient1@example.com", "recipient2@example.com"],
        }
        response = self.client.post("/api/send-email/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Emails sent successfully")

    @patch("anymail.message.AnymailMessage.send")
    def test_send_email_failover1(self, mock_send_mail):
        mock_send_mail.side_effect = [
            AnymailAPIError("Primary failed"),
            AnymailAPIError("Secondary failed"),
            1,
        ]  # Simula fallo del broker primario y éxito en de secundario
        data = {
            "subject": "Test Subject",
            "message": "Test Message",
            "from_email": "test@example.com",
            "recipient_list": ["recipient1@example.com", "recipient2@example.com"],
        }
        response = self.client.post("/api/send-email/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Emails sent successfully")
