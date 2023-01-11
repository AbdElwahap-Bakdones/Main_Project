from ..ModelsGraphQL import typeobject, inputtype
from rest_framework import status as status_code
from django.db.models import Q
from core import models, serializer
from ..Auth.permission import checkPermission
from .. import QueryStructure
import graphene


def GetPlayerByName(name: str) -> list:

    data = models.Player.objects.filter(Q(user_id__first_name=name) | Q(user_id__last_name=name))
    return data


class AddFrien  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.Field(typeobject.PlayerObjectType)

    class Arguments:
        data = inputtype.SearchPlayerInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_friend", user):
                return QueryStructure.NoPermission(self)
            message = 'OK'
            status = status_code.HTTP_200_OK
            if 'player_email' in kwargs:
                data = models.Player.objects.filter(user_id__email=kwargs['player_email'])
                if not data.exists():
                    return QueryStructure.NotFound(self)

            elif 'player_Name' in kwargs:
                data = GetPlayerByName(kwargs['player_Name'])
                if data.__len__ == 0:
                    return QueryStructure.NotFound
            else:
                QueryStructure.BadRequest(self, message='there is no paramiter')
        except Exception as e:
            print('Error in AddClub :')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)
