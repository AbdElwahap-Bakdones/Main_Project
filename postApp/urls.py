
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
urlpatterns = [re_path(r'^id=(?P<pk>[0-9]*)/$', views.posts.as_view()),
               path('signup', views.SignUp.as_view()),
               path('login', views.login),
               path('getAllPost/<int:pk>/<int:index>/', views.getAllPost)]
