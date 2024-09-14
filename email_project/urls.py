from django.urls import path, include
from email_auth.views import CustomTokenRefreshView, CustomTokenObtainPairView
from email_configuration.views import (
    EmailConfigurationListCreateAPIView,
    EmailConfigurationRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("api/", include("email_app.urls")),
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair"),
    path(
        "api/token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh"
    ),
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
