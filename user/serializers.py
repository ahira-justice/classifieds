from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from core.models import Profile
from utils.states import STATE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    state_of_residence = serializers.ChoiceField(write_only=True, required=True, choices=STATE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'state_of_residence')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a basic profile and user with encrypted password and return it"""
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        state_of_residence = validated_data.pop('state_of_residence', None)

        user = get_user_model().objects.create_user(**validated_data)
        Profile.objects.create(user=user, first_name=first_name, last_name=last_name, state_of_residence=state_of_residence)

        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
