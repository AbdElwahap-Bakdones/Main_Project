from core.models import Friend, Player, User
from core import serializer, models
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
        print(data[1])
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


class GetFriendCanAddToTeam(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.FriendConnection, team_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_friend'):
                return QueryFields.rise_error(user)
            team_id = models.Team.objects.filter(
                pk=kwargs['team_id'], deleted=False)
            if not team_id.exists():
                return QueryFields.BadRequest(info=info, msg='Team id not found')
            is_valied = models.Team_members.objects.filter(player_id__user_id=user,
                                                           team_id=team_id.get(), is_captin=True, is_leave=False)
            if not is_valied.exists():
                return QueryFields.BadRequest(info=info, msg='you not in the team or you not a caption in the team!')
            members_player_list = models.Team_members.objects.filter(
                Q(team_id=team_id) & Q(is_leave=False) & ~Q(pk=is_valied.get().pk)).values_list('player_id', flat=True)
            friend_can_add = Friend.objects.filter((Q(player1__user_id=user) & Q(
                state='accepted')) & ~Q(player2__in=members_player_list))
            if friend_can_add.exists():
                return QueryFields.OK(info=info, data=friend_can_add)
            return QueryFields.NotFound(info)
        except Exception as e:
            print('error in GetFriendCanAddToTeam')
            print(str(e))
            return QueryFields.ServerError(info=info, msg=str(e))
