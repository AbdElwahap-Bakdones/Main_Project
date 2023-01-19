from core.models import Club
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from ..Relay import relays
import graphene
from core import models

# player or manager show All clubs in the system
class AllClub(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ClubConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryAll(Club, info, 'core.view_club')

# manager example :in selector add section
class MyClub(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ClubConnection)

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not models.Manager.objects.filter(user_id=user).exists():
            return QueryFields.BadRequest(info=info)
        data = models.Club.objects.filter(manager_id__user_id=user, is_deleted=False)
        return QueryFields.OK(info=info, data=data)

# manager search on club in All yourclub by club name
class GetClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubConnection, name_club=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not models.Manager.objects.filter(user_id=user).exists():
            return QueryFields.BadRequest(info=info)
        data = models.Club.objects.filter(manager_id__user_id=user,name=kwargs["name_club"], is_deleted=False)
        if not data.exists():
          return  QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)

# player search on club by club name
class searchOnClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubConnection, name_club=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_club'):
            return QueryFields.rise_error(user)
        data = Club.objects.filter(
            name=kwargs['name_club'], is_deleted=False, is_available=True)
        if not data.exists():
          return  QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)
