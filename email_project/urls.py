from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from email_configuration.views import (
    EmailConfigurationListCreateAPIView,
    EmailConfigurationRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("api/", include("email_app.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/configuration/",
        EmailConfigurationListCreateAPIView.as_view(),
        name="email-configuration-list-create",
    ),
    path(
        "api/configuration/<pk>",
        EmailConfigurationRetrieveUpdateDestroyAPIView.as_view(),
        name="email-configuration-retrieve-update-destroy",
    ),
    path("health-check/", include("health_check.urls")),
]
