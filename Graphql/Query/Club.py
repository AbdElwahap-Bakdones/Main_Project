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
    pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = Club
        fields = ['id', 'pk']
        interfaces = (relay.Node,)


class ClubConnection(relay.Connection):

    class Meta:
        node = ClubModel


class AllClub(ObjectType, QueryFields):
    data = relay.ConnectionField(ClubConnection, id=graphene.String())

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_clu2b'):
            return QueryFields.rise_error(user)
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'OKK')
        return Club.objects.all()
