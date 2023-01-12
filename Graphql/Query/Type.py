from core.models import Type
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class AllType(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.TypeConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryAll(Type, info, 'core.view_type')
