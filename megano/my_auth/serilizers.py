from django.contrib.auth.models import User
from rest_framework import serializers


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        fields = ['alt', 'src']

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["fullName", "email", "phone", "avatar"]


class ChangePWDSerializer(serializers.Serializer):
    model = User

    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)
