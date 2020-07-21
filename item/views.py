from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist

from item.serializers import ItemSerializer
from core.models import Buyer, Item


class Items(generics.ListCreateAPIView):
    """List all the user created items. Can create new items"""
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Item.objects.filter(user=self.request.user)
        else:
            return Item.objects.filter(is_sold=False).order_by('-created_at')

    def get_permissions(self):
        if self.request.method in ['POST']:
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [AllowAny, ]

        return [permission() for permission in permission_classes]


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """Show a specific item. Can perform update and delete"""
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Item.objects.filter(user=self.request.user)
        else:
            return Item.objects.filter(is_sold=False)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [AllowAny, ]

        return [permission() for permission in permission_classes]


class ShowInterest(APIView):
    def post(self, request):
        id = request.data.get('id', None)
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        location = request.data.get('location', None)

        message = self.validate(id, name, email, location)
        if message:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(id=id)
            buyer = Buyer.objects.create(name=name, email=email, location=location)
            item.buyers.add(buyer)
            data = ItemSerializer(item).data

            return Response(data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            message = {'id': 'Item with provided id does not exist'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

    def validate(self, id, name, email, location):
        message = {}
        if id is None:
            message['id'] = 'Please provide a value for id'
        if name is None:
            message['name'] = 'Please provide a value for name'
        if email is None:
            message['email'] = 'Please provide a value for email'
        if location is None:
            message['location'] = 'Please provide a value for location'

        return message


class MarkAsSold(APIView):
    def post(self, request):
        if not self.request.user.is_authenticated:
            message = {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        id = request.data.get('id', None)

        message = self.validate(id)
        if message:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(id=id)
            item.is_sold = True
            item.save()
            data = ItemSerializer(item).data

            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            message = {'id': 'Item with provided id does not exist'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

    def validate(self, id):
        message = {}
        if id is None:
            message['id'] = 'Please provide a value for id'

        return message
