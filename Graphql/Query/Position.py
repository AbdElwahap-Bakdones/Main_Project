from core.models import Position
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene





class PositionByType(ObjectType, QueryFields):

    data = relay.ConnectionField(
        relays.PositionConnection, type_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_position'):
            return QueryFields.rise_error(user)
        data = Position.objects.filter(type_id=kwargs['type'])
        if not data.exists():
            QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info,data=data)
