from core.models import Friend, Player, User
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
from django.db.models import Q
import graphene


def correct_structure(data, user):
    for i in data:
        if i.player2.user_id == user:
            player = i.player2
            i.player2 = i.player1
            i.player1 = player


class AllFriend(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.FriendConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_friend'):
            return QueryFields.rise_error(user)
        data = Friend.objects.filter(
            Q(player1__user_id=user) & Q(state="accepted"))
        return QueryFields.OK(info, data=data)


class GetFriendByName(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.FriendConnection, name=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_friend'):
            return QueryFields.rise_error(user)
        data = Friend.objects.filter(Q(player1__user_id=user) & Q(state="accepted") &
                                     Q(
            Q(player2__user_id__first_name__iexact=kwargs['name']) |
            Q(player2__user_id__last_name__iexact=kwargs['name'])
        )

        )
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        correct_structure(data, user)
        return data


class GetFriendById(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.FriendConnection, player_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_friend'):
            return QueryFields.rise_error(user)
        data = Friend.objects.filter(
            player2__pk=kwargs['player_id'], state='accepted')
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        correct_structure(data, user)
        return data
