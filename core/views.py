from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from django.contrib.auth.models import Group


def say_hi():
    print('hi')


@api_view(['GET', 'POST'])
def deleteUser(request):
    # User.objects.get(pk=1).delete()
    groups = Group.objects.get(id=3)
    print(groups.name)
    return Response(User.objects.get(username='f15@l15').get_group_permissions())
