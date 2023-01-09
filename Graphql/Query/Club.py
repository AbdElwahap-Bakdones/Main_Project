from core.models import Club
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays


class AllClub(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ClubConnection)

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']