from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profile.serializers import ProfileSerializer
from core.models import Profile


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """Show the authenticated user's profile. Can perform update"""
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
