from ..ModelsGraphQL import typeobject, inputtype
from rest_framework import status as status_code
from graphene import ObjectType, relay
from django.db import models as MODELS
from django.db.models import Q, QuerySet
from core import models, serializer
from django.db.models import Subquery, Value
from ..Relay import relays
from ..QueryStructure import QueryFields
import graphene
from itertools import chain


class SerchPlayer (ObjectType, QueryFields):

    data = relay.ConnectionField(
        relays.PlayerConnection, player_Name=graphene.String(),
        player_Email=graphene.String(),
        without_Friend=graphene.Boolean(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not QueryFields.is_valide(info=info, user=user, operation="core.add_friend"):
                return QueryFields.rise_error(user=user)
            if 'player_Email' in kwargs:
                data = Player(nameORemail=kwargs['player_Email'], user=user,
                              with_no_friend=kwargs['without_Friend']).getPlayerByEmail()
            elif 'player_Name' in kwargs:
                data = Player(
                    nameORemail=kwargs['player_Name'], with_no_friend=kwargs['without_Friend'], user=user).GetPlayerByName()

            else:
                return QueryFields.BadRequest(info=info)
            if data.__len__() <= 0:
                return QueryFields.NotFound(info=info)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('Error in SerchPlayer :')
            print(e)
            return QueryFields.ServerError(info=info, msg=str(e))


class Player:
    def __init__(self, nameORemail: str,  user: models.User, with_no_friend=False):
        print('123')
        self.name = nameORemail
        self.user = user
        self.with_no_friend = with_no_friend

    def getPlayerByEmail(self):
        data = models.Player.objects.filter(
            user_id__email=self.name)
        print(data)
        if not data.exists():
            return[]
        fried = models.Friend.objects.filter(
            player1__user_id=self.user, player2__user_id__email=self.name, state='accepted').values_list('player2__pk', flat=True)
        print(fried)
        return self.add_state_toPlayer(query_set=data, friend_list=fried)

    def GetFriendByName(self) -> models.Friend.objects:

        if self.name.count(' ') > 1:
            return []
        if self.name.__contains__(' '):
            FL_name = self.name.split(sep=' ')
            username = self.name.replace(' ', '@')
            friend = models.Friend.objects.filter(
                Q(player1__user_id=self.user) & Q(state='accepted') &
                (Q(player2__user_id__username__iexact=username) | Q(player2__user_id__first_name__iexact=FL_name[0]) |
                 Q(player2__user_id__last_name__iexact=FL_name[1])))
        else:
            friend = models.Friend.objects.filter(
                Q(player1__user_id=self.user) & Q(state='accepted')
                &
                (Q(player2__user_id__first_name__iexact=self.name) |
                    Q(player2__user_id__last_name__iexact=self.name)))
        return friend

    def GetPlayerByName(self) -> list:
        friend_list = []
        if self.name.count(' ') > 1:
            return []
        elif self.name.__contains__(' '):
            FL_name = self.name.split(sep=' ')
            name = self.name.replace(' ', '@')
            friend = self.GetFriendByName().values_list(
                'player2__pk', flat=True)
            if self.with_no_friend:
                friend_list = friend

            data = models.Player.objects.filter(~Q(user_id=self.user) & ~Q(pk__in=friend_list) &
                                                (Q(user_id__username__iexact=name) |
                                                Q(user_id__first_name__iexact=FL_name[0]) |
                                                Q(user_id__last_name__iexact=FL_name[1])))

        else:
            friend = self.GetFriendByName().values_list(
                'player2__pk', flat=True)
            if self.with_no_friend:
                friend_list = friend
            data = models.Player.objects.filter(~Q(user_id=self.user) & ~Q(pk__in=friend_list) &
                                                (Q(user_id__first_name__iexact=self.name) | Q(user_id__last_name__iexact=self.name)))

        return self.add_state_toPlayer(query_set=data,  friend_list=friend)
        # return data

    def add_state_toPlayer(self, query_set: QuerySet,  friend_list: list):
        player = QuerySet
        pending = self.get_pending_player(query_set=query_set)
        friend = self.get_friend_player(
            query_set=query_set, friend_list=friend_list)
        all_player_list = list(query_set.values_list('pk', flat=True))
        F_P = friend.get('list')+pending.get('list')
        notFriend = self.get_player_notFriend(query_set, all_player_list, F_P)
        player = list(chain(friend.get('objects'), pending.get(
            'objects'), notFriend.get('objects')))

        return player

    def get_friend_player(self, query_set: QuerySet, friend_list: list) -> dict:
        player_friend = query_set.filter(pk__in=friend_list).annotate(
            state=Value('friend', output_field=MODELS.CharField()))
        player_friend_list = list(player_friend.values_list('pk', flat=True))
        return {'objects': player_friend, 'list': player_friend_list}

    def get_pending_player(self, query_set: QuerySet) -> dict:
        all_pending_objets = models.Friend.objects.filter(
            player1__user_id=self.user, player2__in=query_set.values_list('pk', flat=True), state='pending')
        all_player_pending_list = list(
            all_pending_objets.values_list('player2__pk', flat=True))
        pending_request_list = all_pending_objets.filter(
            sender__user_id=self.user).values_list('player2__pk', flat=True)
        pending_recive_list = all_pending_objets.filter(
            ~Q(sender__user_id=self.user)).values_list('player2__pk', flat=True)
        player_pending_request = query_set.filter(
            pk__in=pending_request_list).annotate(state=Value('pending', output_field=MODELS.CharField()))
        player_pending_recive = query_set.filter(
            pk__in=pending_recive_list).annotate(state=Value('accept', output_field=MODELS.CharField()))
        player_pending = list(
            chain(player_pending_recive, player_pending_request))
        return {'objects': player_pending, 'list': all_player_pending_list}

    def get_player_notFriend(self, query_set: QuerySet, all_player_list: list, F_P: list) -> dict:
        player_not_friend_list = list(set(all_player_list) - set(F_P))
        player_not_friend = query_set.filter(pk__in=player_not_friend_list).annotate(state=Value(
            'notFriend', output_field=MODELS.CharField()))
        return {'objects': player_not_friend, 'list': player_not_friend_list}


class me(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.PlayerConnection)

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not QueryFields.is_valide(info=info, user=user, operation="core.add_friend"):
                return QueryFields.rise_error(user=user)
            player_obj = models.Player.objects.filter(user_id=user)
            return QueryFields.OK(info=info, data=player_obj)
        except Exception as e:
            print('Error in Player.me :')
            print(e)
            return QueryFields.ServerError(info=info, msg=str(e))
