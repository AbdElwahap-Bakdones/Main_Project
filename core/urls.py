from django.contrib import admin
from django.urls import path, include, re_path
from . import views
urlpatterns = [
    path('login_view', views.login_view),
    path('csrf', views.csrf)

]
