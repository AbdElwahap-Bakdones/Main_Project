from core.models import Friend
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
from django.db.models import Q
import graphene


class AllFriend(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.FriendConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_friend'):
            return QueryFields.rise_error(user)
        data = Friend.objects.filter(Q(player1__id=user.id) | Q(
            player2__id=user.id) & Q(state="accepted"))
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'okk')
        return data


class GetFriend(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.FriendConnection, name=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_friend'):
            return QueryFields.rise_error(user)
        data = Friend.objects.filter(
            ((Q(player1__id=user.id) &
              (Q(player2__first_name=kwargs['name']) | Q(player2__last_name=kwargs['name']))) |
             ((Q(player1__first_name=kwargs['name']) | Q(player1__last_name=kwargs['name'])) & Q(
                 player2__id=user.id))) & Q(state="accepted"))
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'okk')
        return data
