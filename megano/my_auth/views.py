import json
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework.views import APIView


class SingInView(APIView):

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
