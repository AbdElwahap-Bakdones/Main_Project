from ..ModelsGraphQL import typeobject, inputtype
from rest_framework import status as status_code
from django.db.models import Q
from core import models, serializer
from ..Auth.permission import checkPermission
from .. import QueryStructure
import graphene


def GetFriendByName(name: str,  user: models.User) -> models.Friend.objects:
    if name.count(' ') > 1:
        return []
    elif name.__contains__(' '):
        FL_name = name.split(sep=' ')
        name = name.replace(' ', '@')
        friend = models.Friend.objects.filter(Q(player1__user_id__username=user) & Q(status='accepted') & (Q(player2__user_id__username=name) | Q(
            player2__user_id__first_name=FL_name[0]) | Q(player2__user_id__last_name=FL_name[1])))
    else:
        friend = models.Friend.objects.filter(
            Q(player2__user_id__first_name=name) | Q(player2__user_id__last_name=name))
    return friend


def GetPlayerByName(name: str, with_no_Friend=False, user=None) -> list:
    if name.count(' ') > 1:
        return []
    elif name.__contains__(' '):
        FL_name = name.split(sep=' ')
        name = name.replace(' ', '@')
        friend = []
        if with_no_Friend:
            friend = GetFriendByName(name=name, user=user).values_list(
                'player2__user_id__pk', flat=True)

        data = models.Player.objects.filter(~Q(user_id__pk__in=friend) & (Q(user_id__username=name) | Q(
            user_id__first_name=FL_name[0]) | Q(user_id__last_name=FL_name[1])))

    else:
        data = models.Player.objects.filter(
            Q(user_id__first_name=name) | Q(user_id__last_name=name))
    return data


class AddFrien  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.List(typeobject.PlayerObjectType)

    class Arguments:
        data = inputtype.SearchPlayerInput()

    @ classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_friend", user):
                return QueryStructure.NoPermission(self)
            msg = 'OK'
            status = status_code.HTTP_200_OK
            kwargs = kwargs['data']
            if 'player_email' in kwargs:
                data = models.Player.objects.filter(
                    user_id__email=kwargs['player_email'])
                if not data.exists():
                    return QueryStructure.NotFound(self)
            elif 'player_Name' in kwargs:
                data = GetPlayerByName(
                    kwargs['player_Name'], with_no_Friend=True, user=user)

                if data.__len__() <= 0:
                    return QueryStructure.NotFound(self)
            else:
                return QueryStructure.BadRequest(self, message='there is no paramiter')
        except Exception as e:
            print('Error in AddClub :')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)
