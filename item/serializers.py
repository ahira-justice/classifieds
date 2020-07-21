from rest_framework import serializers
from core.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for the item object"""

    class Meta:
        model = Item
        fields = ('id', 'user', 'name', 'price', 'description', 'url')
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        user = self.context.pop('request', None).user
        return Item.objects.create(user=user, **validated_data)
