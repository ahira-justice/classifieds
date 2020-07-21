from rest_framework import serializers
from core.models import Buyer, Item


class BuyerSerializer(serializers.ModelSerializer):
    """Serializer for the buyer object"""

    class Meta:
        model = Buyer
        exclude = ('id', )


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for the item object"""
    buyers = BuyerSerializer(many=True, required=False)

    class Meta:
        model = Item
        fields = ('id', 'user', 'name', 'price', 'description', 'url', 'buyers')
        read_only_fields = ('id', 'user', 'buyers')

    def create(self, validated_data):
        user = self.context.pop('request', None).user
        return Item.objects.create(user=user, **validated_data)
