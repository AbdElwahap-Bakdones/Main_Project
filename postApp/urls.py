
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [path('<int:pk>/', views.posts.as_view()),
               path('signup', views.SignUp.as_view()),
               path('login', views.login),
               path('getAllPost/<int:pk>/<int:index>/', views.getAllPost)]
