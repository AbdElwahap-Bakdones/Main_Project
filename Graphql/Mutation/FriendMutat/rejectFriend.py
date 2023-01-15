from django.db.models import Q
import graphene
from core import models, serializer
from ...ModelsGraphQL import typeobject, inputtype
from ...Auth.permission import checkPermission
from rest_framework import status as status_code
from ... import QueryStructure


class RejectFriend(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.FriendObjectType)

    class Arguments:
        data = inputtype.AddRequestFriendInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_friend", user):
                return QueryStructure.NoPermission(self)

            reciver = models.Player.objects.filter(
                pk=kwargs['data']['player_pk'])
            sender = models.Player.objects.filter(user_id=user)

            if not reciver.exists() or sender.filter(pk=kwargs['data']['player_pk']).exists():
                return QueryStructure.BadRequest(self, message='maybe player not found !')
            requqest_obj = models.Friend.objects.filter(
                ((Q(player1=sender.get())) & (Q(player2=reciver.get()))) |
                ((Q(player2=sender.get())) & (Q(player1=reciver.get()))))
            if requqest_obj.exists():
                return RejectFriend.__reject_request(self, sender.get(), requqest_obj)
            return QueryStructure.InternalServerError(self)
        except Exception as e:
            print('Error in RejectFriend :')
            print(e)
            return QueryStructure.InternalServerError(self, message=str(e))

    def __reject_request(self, sender: models.Player, request: models.Friend.objects.filter):
        try:
            print('old')
            if request.count() == 2 and not request.first().state == 'rejected':
                request.update(state='rejected')
                return QueryStructure.OK(self, data=request.first())
            return QueryStructure.BadRequest(self)
        except Exception as e:
            print('Error in __reject_request')
            print(e)
            return QueryStructure.InternalServerError(self, message=str(e))
