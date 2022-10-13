from django.urls import include, path
from .views import sayHi
urlpatterns = [
    path('', sayHi, name=''),
]
