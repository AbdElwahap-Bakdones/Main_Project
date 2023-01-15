from ..ModelsGraphQL import typeobject, inputtype
from rest_framework import status as status_code
from graphene import ObjectType, relay
from django.db.models import Q
from core import models, serializer
from ..Relay import relays
from ..QueryStructure import QueryFields
import graphene


class SerchPlayer  (ObjectType, QueryFields):

    data = relay.ConnectionField(
        relays.PlayerConnection, player_Name=graphene.String(), player_Email=graphene.String(), without_Friend=graphene.Boolean(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        try:
            user = info.context.META["user"]
            if not QueryFields.is_valide(info=info, user=user, operation="core.add_friend"):
                return QueryFields.rise_error
            if 'player_email' in kwargs:
                data = models.Player.objects.filter(
                    user_id__email=kwargs['player_email'])
                if not data.exists():
                    return QueryFields.NotFound(info=info)
            elif 'player_Name' in kwargs:
                data = GetPlayerByName(
                    kwargs['player_Name'], with_no_Friend=kwargs['without_Friend'], user=user)

                if data.__len__() <= 0:
                    return QueryFields.NotFound(info=info)
            else:
                return QueryFields.BadRequest(info=info)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('Error in SerchPlayer :')
            print(e)
            return QueryFields.ServerError(info=info, msg=str(e))


def GetFriendByName(name: str,  user: models.User) -> models.Friend.objects:
    if name.count(' ') > 1:
        return []
    if name.__contains__(' '):
        FL_name = name.split(sep=' ')
        name = name.replace(' ', '@')
        friend = models.Friend.objects.filter(
            Q(player1__user_id=user) & Q(state='accepted') &
            (Q(player2__user_id__username__iexact=name) | Q(player2__user_id__first_name__iexact=FL_name[0]) |
             Q(player2__user_id__last_name__iexact=FL_name[1])))
    else:
        print(name)
        print(type(user))
        friend = models.Friend.objects.filter(
            Q(player1__user_id=user) & Q(state='accepted')
            &
            (Q(player2__user_id__first_name__iexact=name) |
                Q(player2__user_id__last_name__iexact=name)))
    print(friend)
    return friend


def GetPlayerByName(name: str, with_no_Friend=False, user=None) -> list:
    print(with_no_Friend)
    if name.count(' ') > 1:
        return []
    elif name.__contains__(' '):
        FL_name = name.split(sep=' ')
        name = name.replace(' ', '@')
        friend = []
        if with_no_Friend:
            friend = GetFriendByName(name=name, user=user).values_list(
                'player2__pk', flat=True)

        data = models.Player.objects.filter(~Q(user_id=user) & ~Q(pk__in=friend) & (Q(user_id__username__iexact=name) | Q(
            user_id__first_name__iexact=FL_name[0]) | Q(user_id__last_name__iexact=FL_name[1])))

    else:
        friend = []
        if with_no_Friend:
            friend = GetFriendByName(name=name, user=user).values_list(
                'player2__pk', flat=True)
        print(friend)
        data = models.Player.objects.filter(~Q(user_id=user) & ~Q(pk__in=friend) &
                                            (Q(user_id__first_name__iexact=name) | Q(user_id__last_name__iexact=name)))
    return data
