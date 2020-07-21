from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from uuid import uuid4 as uid

from core.models import Item
from item.serializers import ItemSerializer


ITEMS_URL = reverse('item:collection')


class PublicItemApiTests(TestCase):
    """Test the publicly available items API"""

    def setUp(self):
        self.client = APIClient()
        self.resource_id = uid()

    def test_retrieve_item_list_buyer(self):
        """Test retrieving a list of items by a buyer is successful"""
        user = get_user_model().objects.create_user('test1@c2c.com', 'testpassword')
        Item.objects.create(
            user=user,
            name='Test Item1',
            price=12,
            description='Item1 description',
            url='c2c.com/static/item1.jpg'
        )
        Item.objects.create(
            user=user,
            name='Test Item2',
            price=12,
            description='Item2 description',
            url='c2c.com/static/item2.jpg'
        )

        res = self.client.get(ITEMS_URL)
        items = Item.objects.all().order_by('-created_at')
        serializer = ItemSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_login_required_to_create_item(self):
        """Test that login is required for creating an item"""
        res = self.client.post(ITEMS_URL, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_item_buyer(self):
        """Test retrieving an item by a buyer is successful"""
        user = get_user_model().objects.create_user('test1@c2c.com', 'testpassword')
        item = Item.objects.create(
            user=user,
            name='Test Item',
            price=12,
            description='Item description',
            url='c2c.com/static/item.jpg'
        )
        RESOURCE_URL = reverse('item:resource', args=[item.id])

        res = self.client.get(RESOURCE_URL)
        serializer = ItemSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_login_required_to_update_item(self):
        """Test that login is required for updating an item"""
        RESOURCE_URL = reverse('item:resource', args=[self.resource_id])
        res = self.client.put(RESOURCE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_to_delete_item(self):
        """Test that login is required to delete an item"""
        RESOURCE_URL = reverse('item:resource', args=[self.resource_id])
        res = self.client.delete(RESOURCE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemApiTests(TestCase):
    """Test the authorized user items API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@c2c.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_item_list_seller(self):
        """Test retrieving a list of items by a seller is successful"""
        Item.objects.create(
            user=self.user,
            name='Test Item1',
            price=12,
            description='Item1 description',
            url='c2c.com/static/item1.jpg'
        )
        Item.objects.create(
            user=self.user,
            name='Test Item2',
            price=12,
            description='Item2 description',
            url='c2c.com/static/item2.jpg'
        )

        res = self.client.get(ITEMS_URL)
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_item_seller_valid(self):
        """Test creating a new item with valid parameters by a seller passes"""
        payload = {
            'name': 'Test Item',
            'price': 12,
            'description': 'Item description',
            'url': 'c2c.com/static/item.jpg'
        }

        res = self.client.post(ITEMS_URL, payload)

        item = Item.objects.filter(name=payload['name'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(item.exists())

    def test_create_item_seller_invalid(self):
        """Test creating invalid item by a seller fails"""
        payload = {
            'name': '',
            'price': 12,
            'description': 'Item description',
            'url': 'c2c.com/static/item.jpg'
        }

        res = self.client.post(ITEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_item_seller(self):
        """Test retrieving an item by a buyer is successful"""
        item = Item.objects.create(
            user=self.user,
            name='Test Item',
            price=12,
            description='Item description',
            url='c2c.com/static/item.jpg'
        )
        RESOURCE_URL = reverse('item:resource', args=[item.id])

        res = self.client.get(RESOURCE_URL)
        serializer = ItemSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_item_seller_not_creator(self):
        """Test retrieving an item by a seller created by another seller fails"""
        user = get_user_model().objects.create_user('test1@c2c.com', 'testpassword')
        item = Item.objects.create(
            user=user,
            name='Test Item Other Seller',
            price=12,
            description='Item description',
            url='c2c.com/static/item.jpg'
        )
        RESOURCE_URL = reverse('item:resource', args=[item.id])

        res = self.client.get(RESOURCE_URL)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item_seller(self):
        """Test updating an item with valid parameters by a seller passes"""
        item = Item.objects.create(
            user=self.user,
            name='Test Item Other Seller',
            price=12,
            description='Item description',
            url='c2c.com/static/item.jpg'
        )
        RESOURCE_URL = reverse('item:resource', args=[item.id])

        payload = {
            'name': 'Updated Item Name',
            'url': 'c2c.com/static/updated-item.jpg'
        }

        res = self.client.patch(RESOURCE_URL, payload)
        item.refresh_from_db()
        serializer = ItemSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_item_staffuser(self):
        """Test deleting an item by a seller passes"""
        item = Item.objects.create(
            user=self.user,
            name='Test Item Other Seller',
            price=12,
            description='Item description',
            url='c2c.com/static/item.jpg'
        )
        RESOURCE_URL = reverse('item:resource', args=[item.id])

        res = self.client.delete(RESOURCE_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
