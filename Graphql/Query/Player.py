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
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D


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
                data = Player(user=user).getPlayerByEmail(
                    email=kwargs['player_Email'])
            elif 'player_Name' in kwargs:
                data = Player(user=user).GetPlayerByName(
                    nameORemail=kwargs['player_Name'], with_no_friend=kwargs['without_Friend'])

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
    def __init__(self, user: models.User):
        self.user = user
        # print('init player')

    def getPlayerById(self, id: int) -> models.Player:
        player_obj = models.Player.objects.filter(id=id)
        if not player_obj.exists():
            return[]
        return self.add_state_toPlayer(player_obj)

    def getPlayerByEmail(self, email: str):
        data = models.Player.objects.filter(
            user_id__email=email)
        if not data.exists():
            return[]
        return self.add_state_toPlayer(query_set=data)

    def GetPlayerByName(self, nameORemail: str, with_no_friend=False) -> list:
        name = nameORemail
        friend_list = []
        if name.count(' ') > 1:
            return []
        if name.__contains__(' '):
            FL_name = name.split(sep=' ')
            name = name.replace(' ', '@')
            data = models.Player.objects.filter(~Q(user_id=self.user) &
                                                (Q(user_id__username__iexact=name) |
                                                Q(user_id__first_name__iexact=FL_name[0]) |
                                                Q(user_id__last_name__iexact=FL_name[1])))

        else:
            data = models.Player.objects.filter(~Q(user_id=self.user) &
                                                (Q(user_id__first_name__iexact=name) | Q(user_id__last_name__iexact=name)))

        if with_no_friend:
            friend_list = self.get_friend_player(data)['list']
        data = data.filter(~Q(pk__in=friend_list))
        return self.add_state_toPlayer(query_set=data)
        # return data

    def add_state_toPlayer(self, query_set: QuerySet):
        player = QuerySet
        pending = self.get_pending_player(query_set=query_set)
        friend = self.get_friend_player(
            query_set=query_set)
        all_player_list = list(query_set.values_list('pk', flat=True))
        F_P = friend.get('list')+pending.get('list')
        notFriend = self.get_player_notFriend(query_set, all_player_list, F_P)
        player = list(chain(friend.get('objects'), pending.get(
            'objects'), notFriend.get('objects')))

        return player

    def get_friend_player(self, query_set: QuerySet) -> dict:
        player_list = query_set.values_list('pk', flat=True)
        friend_list = models.Friend.objects.filter(
            player1__user_id=self.user, player2__in=player_list, state='accepted').values_list('player2__pk', flat=True)
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
            if not QueryFields.is_valide(info=info, user=user, operation="core.view_player"):
                return QueryFields.rise_error(user=user)
            player_obj = models.Player.objects.filter(user_id=user)
            return QueryFields.OK(info=info, data=player_obj)
        except Exception as e:
            print('Error in Player.me :')
            print(e)
            return QueryFields.ServerError(info=info, msg=str(e))


class GeoPlayer(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.PlayerConnection, location_lat=graphene.String(
        required=True), location_long=graphene.String(required=True), distance=graphene.Float(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not QueryFields.is_valide(info=info, user=user, operation="core.view_player"):
                return QueryFields.rise_error(user=user)

            pnt = GEOSGeometry(
                "POINT("+kwargs['location_lat']+" " + kwargs['location_long']+")", srid=32140)
            all_player = models.Player.objects.filter(Q(point__distance_lte=(
                pnt, D(km=kwargs['distance'])), available_on_map=True))
            if not all_player.exists():
                return QueryFields.NotFound(info)
            data = Player(user=user).add_state_toPlayer(
                query_set=all_player)
            return QueryFields.OK(info, data=data)

        except Exception as e:
            print('Error in Player.GeoPlayer :')
            print(e)
            return QueryFields.ServerError(info=info, msg=str(e))


'''user = info.context.META["user"]
if not QueryFields.is_valide(info=info, user=user, operation="core.view_player"):
    return QueryFields.rise_error(user=user)

pnt = GEOSGeometry(
    "POINT("+kwargs['location_lat']+" " + kwargs['location_long']+")", srid=32140)
data = models.Player.objects.filter(~Q(pk=user.pk) and Q(point__distance_lte=(
    pnt, D(km=kwargs['distance'])), available_on_map=True))
if not data.exists():
    return QueryFields.NotFound(info)
return QueryFields.OK(info, data=data)'''

# def GetFriendByName(self, name: str) -> models.Friend.objects:

#     if name.count(' ') > 1:
#         return []
#     if name.__contains__(' '):
#         FL_name = name.split(sep=' ')
#         username = name.replace(' ', '@')
#         friend = models.Friend.objects.filter(
#             Q(player1__user_id=self.user) & Q(state='accepted') &
#             (Q(player2__user_id__username__iexact=username) | Q(player2__user_id__first_name__iexact=FL_name[0]) |
#              Q(player2__user_id__last_name__iexact=FL_name[1])))
#     else:
#         friend = models.Friend.objects.filter(
#             Q(player1__user_id=self.user) & Q(state='accepted')
#             &
#             (Q(player2__user_id__first_name__iexact=name) |
#                 Q(player2__user_id__last_name__iexact=name)))
#     return friend
