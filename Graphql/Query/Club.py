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


class searchOnClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubConnection, name=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_club'):
            return QueryFields.rise_error(user)
        data = Club.objects.filter(
            name=kwargs['name'], is_deleted=False, is_available=True)
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
