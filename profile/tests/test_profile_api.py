from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Profile
from profile.serializers import ProfileSerializer

ME_URL = reverse('profile:me')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


def create_profile(**param):
    return Profile.objects.create(**param)


class PublicProfileApiTests(TestCase):
    """Test the publicly available profile API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_retrieve_profile(self):
        """Test that login is required for retrieving a profile"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_update_profile(self):
        """Test that login is required for updating a profile"""
        res = self.client.put(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProfileApiTests(TestCase):
    """Test the authorized user profile API"""

    def setUp(self):
        self.user = create_user(
            email='test@c2c.com',
            password='password'
        )
        self.profile = create_profile(
            user=self.user,
            first_name='Test',
            last_name='User',
            state_of_residence='LA'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_profile_owner(self):
        """Test retrieving a profile by owner is successful"""
        res = self.client.get(ME_URL)
        serializer = ProfileSerializer(self.profile)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_profile_owner(self):
        """Test updating a profile by owner is successful"""
        payload = {
            'first_name': 'Test',
            'last_name': 'User'
        }

        res = self.client.patch(ME_URL, data=payload)
        self.profile.refresh_from_db()
        serializer = ProfileSerializer(self.profile)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
