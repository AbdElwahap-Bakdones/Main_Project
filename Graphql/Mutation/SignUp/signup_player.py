from core import  serializer
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

class SignUpPlayer(SerializerMutation):
    class Meta:
        serializer_class =serializer.PlayerSerializer