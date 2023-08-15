from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Профиля"""

    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    def get_avatar(self, obj):
        if obj.avatar:
            return {"src": obj.avatar.url, "alt": obj.avatar.name}
        return None


class ChangePWDSerializer(serializers.Serializer):
    """Сериализатор для смены пароля пользователя"""

    currentPassword = serializers.CharField(max_length=200, required=True)
    newPassword = serializers.CharField(max_length=200, required=True)
