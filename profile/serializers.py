from rest_framework import serializers
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile object"""
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('user',  'email', 'first_name', 'last_name', 'state_of_residence')
        read_only_fields = ('user', )

    def get_email(self, obj):
        return self.instance.user.email
