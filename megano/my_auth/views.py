import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework.views import APIView

from my_auth.models import Profile


class SignInView(APIView):
    """Представление для авторизации пользователя"""

    def post(self, request) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """Представление для регистрации пользователя"""

    def post(self, request) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, first_name=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return HttpResponse(status=200)
