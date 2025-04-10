# services\users\interfaces\serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'profile_image', 'password']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'bio': {'required': False},
            'profile_image': {'required': False},
        }
