from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


def say_hi():
    print('hi')


@api_view(['GET', 'POST'])
def deleteUser(request):
    # User.objects.get(pk=1).delete()
    return Response(User.objects.all().values())
