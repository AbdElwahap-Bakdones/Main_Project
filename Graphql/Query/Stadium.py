from core.models import Stadium, Duration
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class GetStadiumByType(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, type=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryAll(Stadium, info, 'core.view_stadium')

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_stadium'):
            return QueryFields.rise_error(user)
        data = Stadium.objects.filter(
            type_id__id=kwargs['type'], is_deleted=False, is_available=True)
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
