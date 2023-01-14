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
            requqest_obj = models.Friend.objects.filter(
                ((Q(player1__user_id=user)) & (Q(player2__pk=pk))) |
                (((Q(player2__user_id=user)) & (Q(player1__pk=pk)))))
            if requqest_obj.exists():
                addRequestFriend.__create_old_request(user, requqest_obj)

        except Exception as e:
            print('Error in addRequestFriend :')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)

    def __create_old_request(sender: models.User, request: models.Friend.objects.filter):
        # if request.first().state == 'pending' or request.first().state == 'accepted':
        try:
            if request.count() == 2 and request.first().state == 'rejected':
                request.update(state='pending', sender=models.Player.objects.filter(user_id=sender).get())
                return QueryStructure.OK(self)
        except Exception as e:
            print('Error in __create_old_request')
            print(e)
        return QueryStructure.BadRequest(self)
