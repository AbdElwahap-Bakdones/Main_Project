from django.db.models import Q
import graphene
from core import models, serializer
from ...ModelsGraphQL import typeobject, inputtype
from ...Auth.permission import checkPermission
from rest_framework import status as status_code
from ... import QueryStructure


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

            reciver = models.Player.objects.filter(
                pk=kwargs['data']['player_pk'])
            sender = models.Player.objects.filter(user_id=user)

            if not reciver.exists() or sender.filter(pk=kwargs['data']['player_pk']).exists():
                return QueryStructure.BadRequest(self, message='maybe player not found !')
            requqest_obj = models.Friend.objects.filter(
                ((Q(player1=sender.get())) & (Q(player2=reciver.get()))) |
                ((Q(player2=sender.get())) & (Q(player1=reciver.get()))))
            if requqest_obj.exists():
                return addRequestFriend.__create_old_request(self, sender.get(), requqest_obj)
            else:
                return addRequestFriend.__create_new_request(self, sender.get(), reciver.get())
            return QueryStructure.InternalServerError(self)
        except Exception as e:
            print('Error in addRequestFriend :')
            print(e)
            return QueryStructure.InternalServerError(self, message=str(e))

    def __create_old_request(self, sender: models.Player, request: models.Friend.objects.filter):
        try:
            print('old')
            if request.count() == 2 and request.first().state == 'rejected':
                request.update(state='pending', sender=sender)
                return QueryStructure.Created(self, data=request.first())
            return QueryStructure.BadRequest(self)
        except Exception as e:
            print('Error in __create_old_request')
            print(e)
            return QueryStructure.InternalServerError(self, message=str(e))

    def __create_new_request(self, sender: models.Player, reciver: models.Player):
        print('new')

        data_ser1 = {}
        data_ser2 = {}
        data_ser1['player1'] = sender.pk
        data_ser1['player2'] = reciver.pk
        data_ser1['state'] = 'pending'
        data_ser1['sender'] = sender.pk
        ser1 = serializer.FrienfSerializer(data=data_ser1)
        data_ser2['player1'] = reciver.pk
        data_ser2['player2'] = sender.pk
        data_ser2['state'] = 'pending'
        data_ser2['sender'] = sender.pk
        ser2 = serializer.FrienfSerializer(data=data_ser2)
        try:
            isValied1 = ser1.is_valid()
            isValied2 = ser2.is_valid()

            if isValied1 and isValied2:
                ser1.validated_data
                data = ser1.save()
                ser2.validated_data
                ser2.save()
                return QueryStructure.Created(instanse=self, data=data)
            else:
                return QueryStructure.BadRequest(self, message=str(ser1.errors))
        except Exception as e:
            print('Error in __create_new_request')
            print(e)
            return QueryStructure.InternalServerError(self, message=str(e))
        return QueryStructure.InternalServerError(self)
