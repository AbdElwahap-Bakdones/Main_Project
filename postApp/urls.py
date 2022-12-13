
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
urlpatterns = [
    path('', views.posts.as_view()),
    # path(r'<int:pk>/', views.posts.as_view()),
    # path('signup', views.SignUp.as_view()),
    # path('login', views.login),
    # #path('getAllPost/<int:index>/', views.getAllPost),
    # path('getMyPosts/<int:pk>/<int:index>/', views.getMyPosts)
]
