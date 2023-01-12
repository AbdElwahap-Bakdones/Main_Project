from django.db.models import Q
import graphene
from core import models, serializer
from ..ModelsGraphQL import typeobject, inputtype
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure


class addRequestFriend(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.FriendObjectType)

    class Arguments:
        data = inputtype.AddRequestFriendInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_friend", user):
                return QueryStructure.NoPermission(self)
            pk = kwargs['player_pk']
            # is_valide = models.Friend(Q(player1__user_id=user)& Q(pl))
        except Exception as e:
            print('Error in addRequestFriend :')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)
