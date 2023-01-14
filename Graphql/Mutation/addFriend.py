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
            print(kwargs)
            pk = kwargs['data']['player_pk']
            requqest_obj = models.Friend.objects.filter(
                ((Q(player1__user_id=user)) & (Q(player2__pk=pk))) |
                (((Q(player2__user_id=user)) & (Q(player1__pk=pk)))))
            if requqest_obj.exists():
                return addRequestFriend.__create_old_request(self, user, requqest_obj)
            else:
                return addRequestFriend.__create_new_request(self, user, pk)
            return QueryStructure.InternalServerError(self)
        except Exception as e:
            print('Error in addRequestFriend :')
            print(e)
            return QueryStructure.InternalServerError(self, msg=str(e))

    def __create_old_request(self, sender: models.User, request: models.Friend.objects.filter):
        # if request.first().state == 'pending' or request.first().state == 'accepted':
        try:
            if request.count() == 2 and request.first().state == 'rejected':
                request.update(state='pending', sender=models.Player.objects.filter(
                    user_id=sender).get())
                return QueryStructure.OK(self)
        except Exception as e:
            print('Error in __create_old_request')
            print(e)
        return QueryStructure.BadRequest(self)

    def __create_new_request(self, sender: models.User, reciver: models.Player):
        data_ser1 = {}
        data_ser2 = {}
        sender = models.Player.objects.get(user_id=sender)
        data_ser1['player1'] = sender
        data_ser1['player2'] = reciver
        data_ser1['state'] = 'pending'
        data_ser1['sender'] = sender
        ser1 = serializer.FrienfSerializer(data=data_ser1)
        data_ser2['player1'] = reciver
        data_ser2['player2'] = sender
        data_ser2['state'] = 'pending'
        data_ser2['sender'] = sender
        ser2 = serializer.FrienfSerializer(data=data_ser1)
        try:
            if ser1.is_valid() and ser2.is_valid():
                ser1.validated_data
                ser1.save()
                ser2.validated_data
                ser2.save()
                return QueryStructure.Created(self)
        except Exception as e:
            print('Error in __create_new_request')
            print(e)
            return QueryStructure.InternalServerError(self, msg=str(e))
        return QueryStructure.InternalServerError(self)
