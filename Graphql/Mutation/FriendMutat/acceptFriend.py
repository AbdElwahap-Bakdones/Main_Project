from django.db.models import Q
import graphene
from core import models, serializer
from ...ModelsGraphQL import typeobject, inputtype
from ...Auth.permission import checkPermission
from rest_framework import status as status_code
from ... import QueryStructure
from notification.notification import Notification


class AcceptFriend(graphene.Mutation, QueryStructure.Attributes):
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
                return AcceptFriend.__accept_request(self, sender.get(), requqest_obj)
            return QueryStructure.InternalServerError(self)
        except Exception as e:
            print('Error in AcceptFriend :')
            print(e)
            return QueryStructure.InternalServerError(self, message=str(e))

    def __accept_request(self, sender: models.Player, request: models.Friend.objects.filter):
        try:
            print('old')
            if request.count() == 2 and not request.first().sender == sender and request.first().state == 'pending':
                request.update(state='accepted')
                self.__send_notif(self, request)
                return QueryStructure.OK(self, data=request.first())
            return QueryStructure.BadRequest(self)
        except Exception as e:
            print('Error in __accept_request')
            print(e)
            return QueryStructure.InternalServerError(self, message=str(e))

    def __send_notif(self, request: models.Friend.objects.filter):
        try:
            print('__send_notif')
            sender = request.first().sender
            reciver = request.first().player2
            if sender == request.first().player2:
                reciver = request.first().player1
            Notification.add(sender=sender.user_id.pk, reciver=reciver.user_id.pk,
                             message=f'{sender.user_id.first_name} {sender.user_id.last_name}   has Accepted your request friend !', sender_kind='user', type='accept friend')

        except Exception as e:
            print('Error in AcceptFriend.__send_notif')
            print(str(e))
