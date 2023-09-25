import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from .serializers import ProfileSerializer, ChangePWDSerializer
from auth_app.models import Profile


class SignInView(APIView):
    """Представление для авторизации пользователя"""

    def post(self, request) -> Response:
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """Представление для регистрации пользователя"""

    def post(self, request) -> Response:
        user_data = json.loads(request.body)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    """Представление для выхода пользователя из аккаунта"""
    logout(request)
    return HttpResponse(status=200)


class ProfileApiView(APIView):
    """Представление для отображения и обновления профиля пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePWDView(APIView):
    """
    Представление для смены пароля пользователя
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePWDSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(raw_password=request.data["newPassword"])
            user.save()
            return Response(status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAvatarView(APIView):
    """Представление для изменения аватара пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        file = request.FILES["avatar"]
        if file is not None:
            profile.avatar = request.FILES["avatar"]
            profile.save()
            return Response(status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
