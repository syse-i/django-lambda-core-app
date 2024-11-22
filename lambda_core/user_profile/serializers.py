from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('avatar',)


class UserProfileCreateSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    def create(self, validated_data):
        avatar = validated_data.get('avatar')
        user_id = validated_data.get('user')
        if avatar and user_id:
            try:
                profile = UserProfile.objects.get(user_id=user_id)
                profile.avatar = avatar
                profile.save()
                return profile
            except UserProfile.DoesNotExist:
                return UserProfile.objects.create(user_id=user_id, avatar=avatar)
        return False

    class Meta:
        model = UserProfile
        fields = ('avatar', 'user',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'groups', 'profile',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name',)


class AccountSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile', 'last_login',)
