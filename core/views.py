from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from main_project.settings import SECRET_KEY
import jwt
from django.contrib.auth.models import Group


def say_hi():
    print('hi')


# cookieapp/views.py


@api_view(['GET'])
def csrf(request):
    response = Response({"message": "Set CSRF cookie"})
    response["X-CSRFToken"] = get_token(request)
    print(response.cookies)
    return response


@api_view(['POST'])
def login_view(request):
    username = request.data['username']
    password = request.data['password']
    print(request.user)
    print('0000000')
    user = authenticate(username=username, password=password)
    if user:
        print(user)
        login(request, user)
        print(user.is_authenticated)

        return Response({'message': 'User logged in', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid username or password', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
