from core.models import Club
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class AllClub(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ClubConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryAll(Club, info, 'core.view_club')


class GetClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryGet(Club, info, 'core.view_club', kwargs["id"])
