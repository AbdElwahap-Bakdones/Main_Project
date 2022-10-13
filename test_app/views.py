from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def hello():
    print('hii')


def sayHi(request):
    print('sayhi')
    return HttpResponse({'final project with \tGhaith - Zaher - Riad - AbdElwahap'})
