from django.db.models import Q
import graphene
from core import models, serializer
from ...ModelsGraphQL import typeobject, inputtype
from ...Auth.permission import checkPermission
from rest_framework import status as status_code
from ... import QueryStructure


class UnFriend(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.FriendObjectType)

    class Arguments:
        data = inputtype.UnFriendInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            pass
            user = info.context.META["user"]
            if not checkPermission("core.change_friend", user):
                return QueryStructure.NoPermission(self)
            friend_id = kwargs['data']['pk']
            friend_obj = models.Friend.objects.filter(
                player1__user_id=user, player2=friend_id, state='accepted')
        except Exception as e:
            print('Error in UnFriend !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))
