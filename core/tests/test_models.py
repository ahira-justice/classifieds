from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class UserModelTests(TestCase):
    """Test class for the User model"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = 'test@c2c.com'
        password = 'testpassword'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@C2C.COM'
        user = get_user_model().objects.create_user(email, 'testpassword')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpassword')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@c2c.com',
            'testpassword'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class ProfileModelTests(TestCase):
    """Test class for the Profile model"""

    def test_profile_str(self):
        """Test the profile string representation"""
        user = get_user_model().objects.create_user('test@c2c.com', 'testpassword')
        profile = models.Profile.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            state_of_residence='LA'
        )

        self.assertEqual(str(profile), profile.user.email)


class ItemModelTests(TestCase):
    """Test class for the Item model"""

    def test_item_str(self):
        """Test the item string representation"""
        user = get_user_model().objects.create_user('test@c2c.com', 'testpassword')
        item = models.Item.objects.create(
            user=user,
            name='Test Item',
            price=12,
            description='Item description',
            url='c2c.com/static/item.jpg'
        )

        self.assertEqual(str(item), item.name)


class BuyerModelTests(TestCase):
    """Test class for the Buyer model"""

    def test_buyer_str(self):
        """Test the buyer string representation"""
        buyer = models.Buyer.objects.create(
            name='Test Buyer',
            email='test@c2c.com',
            location='Lagos'
        )

        self.assertEqual(str(buyer), buyer.name)
