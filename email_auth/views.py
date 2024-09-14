from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "refresh" not in response.data:
            user = request.user
            tokens = get_tokens_for_user(user)
            response.data["refresh"] = tokens["refresh"]
        return response
