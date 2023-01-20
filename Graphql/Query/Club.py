from core.models import Club
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from ..Relay import relays
import graphene
from core import models


class AllClub(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ClubConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryAll(Club, info, 'core.view_club')


class MyClub(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ClubConnection)

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not models.Manager.objects.filter(user_id=user).exists():
            return QueryFields.BadRequest(info=info)
        data = models.Club.objects.filter(manager_id__user_id=user.pk, is_deleted=False)
        return QueryFields.OK(info=info, data=data)


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
            QueryFields.NotFound(info=info)
        QueryFields.OK(info=info, data=data)
