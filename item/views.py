from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from item.serializers import ItemSerializer
from core.models import Item


class Items(generics.ListCreateAPIView):
    """List all the user created items. Can create new items"""
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Item.objects.filter(user=self.request.user)

        return Item.objects.all().order_by('-created_at')

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
            return Item.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [AllowAny, ]

        return [permission() for permission in permission_classes]
