from core.models import Club, Manager
from graphene import ObjectType, relay
from graphene_django.types import DjangoObjectType
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code

import graphene


class ManagerModel(DjangoObjectType):
    class Meta:
        model = Manager
        fields = ['id']


class ClubModel(DjangoObjectType):
    manager_id = graphene.Field(ManagerModel)

    class Meta:
        model = Club
        fields = ['id', 'name', 'location',
                  'number_stad', 'is_available', 'manager_id']
        interfaces = (relay.Node,)


class ClubConnection(relay.Connection):

    class Meta:
        node = ClubModel


class AllClub(ObjectType, QueryFields):
    data = relay.ConnectionField(ClubConnection)

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, '123'):
            return QueryFields.rise_error(user)
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'OKK')
        return Club.objects.all()
