from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUser(generics.CreateAPIView):
    """Create new users"""
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    """Show the authenticated user. Can perform update"""
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class CreateToken(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
