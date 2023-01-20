from core.models import Position
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class AllPosition(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.PositionConnection, type=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryAll(Position, info, 'core.view_position')

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_position'):
            return QueryFields.rise_error(user)
        data = Position.objects.filter(type_id=kwargs['type'])
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data


class PositionByType(ObjectType, QueryFields):

    data = relay.ConnectionField(
        relays.PositionConnection, type_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.OK(info)
