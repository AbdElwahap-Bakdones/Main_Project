from ..ModelsGraphQL import typeobject, inputtype
from graphene import ObjectType, relay
from core import models, serializer
from ..Relay import relays
from ..QueryStructure import QueryFields
import graphene
from django.db.models import Q
from .PlayerClass import Player
from django.contrib.gis.geos import GEOSGeometry, Point
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
                print('rererererere')
                return QueryFields.NotFound(info=info)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('Error in SerchPlayer :')
            print(e)
            return QueryFields.ServerError(info=info, msg=str(e))


class GetPlayerById(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.PlayerConnection, player_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not QueryFields.is_valide(info=info, user=user, operation="core.view_player"):
                return QueryFields.rise_error(user=user)
            query_set = models.Player.objects.filter(pk=kwargs['player_id'])
            if query_set.exists():
                data = Player(user=user).add_state_toPlayer(query_set)
                return QueryFields.OK(info=info, data=data)
            return QueryFields.NotFound(info=info)
        except Exception as e:
            print('Error in GetPlayerById')
            print(str(e))
            return QueryFields.ServerError(info=info, msg=str(e))


class GeoPlayer(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.PlayerConnection, location_lat=graphene.String(
        required=True), location_long=graphene.String(required=True), distance=graphene.Float(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not QueryFields.is_valide(info=info, user=user, operation="core.view_player"):
                return QueryFields.rise_error(user=user)
            # pnt = GEOSGeometry(
            #     "POINT("+kwargs['location_lat']+" " + kwargs['location_long']+")", srid=32140)
            pnt = Point(kwargs['location_lat'],
                        kwargs['location_long'], srid=32140)
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
