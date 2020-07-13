from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Profile

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_valid(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@c2c.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'state_of_residence': 'LA'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        user = get_user_model().objects.get(**res.data)
        profile_exists = Profile.objects.filter(user=user).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertTrue(profile_exists)
        self.assertNotIn('password', res.data)

    def test_create_user_invalid_alreadyexists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test4@c2c.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_passwordtooshort(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'test5@c2c.com', 'password': 'pw'}

        res = self.client.post(CREATE_USER_URL, payload)

        user = get_user_model().objects.filter(
            email=payload['email']
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user.exists())

    def test_login_required_to_retrieve_user(self):
        """Test that login is required for retrieving a user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_update_user(self):
        """Test that login is required for updating a user"""
        res = self.client.put(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_valid(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test6@c2c.com', 'password': 'testpassword'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_valid_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test7@c2c.com', 'password': 'testpassword'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_invalid_wrongpassword(self):
        """Test that token is not created if wrong password is given"""
        create_user(email='test8@c2c.com', password='testpassword')
        payload = {'email': 'test8@c2c.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_invalid_missingfield(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': '', 'password': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)


class PrivateUserApiTests(TestCase):
    """Test user API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@c2c.com',
            password='testpassword',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        res.data.pop('id')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'email': self.user.email})

    def test_update_user(self):
        """Test updating the user profile for authenticated user"""
        payload = {'password': 'newpassword'}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
