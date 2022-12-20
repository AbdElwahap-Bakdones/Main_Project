from core import models
from graphene_django import DjangoObjectType
import graphene


class UserModel(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ['pk', 'first_name', 'last_name',
                  'email', 'phone', 'username']


class UserInput(graphene.InputObjectType):
    first_name = graphene.String(requierd=True)
    last_name = graphene.String(requierd=True)
    email = graphene.String(requierd=True)
    phone = graphene.Int(requierd=True)
    password = graphene.String(requierd=True)


class PlayerInput(graphene.InputObjectType):
    location_lat = graphene.String(requierd=True)
    location_long = graphene.String(requierd=True)


class PlayerModel(DjangoObjectType):
    class Meta:
        model = models.Player
        fields = ['location_lat', 'location_long', 'user_id']


class ManagerModel(DjangoObjectType):
    class Meta:
        model = models.Manager
        fields = ['user_id']


class ManagerInput(graphene.InputObjectType):
    field = graphene.String(requierd=False)
