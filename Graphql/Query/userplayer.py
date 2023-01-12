from core.models import Player
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class GetPlayer(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.PlayerConnection, username=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_player'):
            return QueryFields.rise_error(user)
        data = Player.objects.filter(
            user_id__username=kwargs['username'], deleted=False)
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
