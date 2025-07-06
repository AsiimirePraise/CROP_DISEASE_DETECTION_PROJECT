
from rest_framework import serializers
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'user_type', 'phone', 'location', 'farm_size',
            'crops_grown', 'profile_picture', 'bio', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
