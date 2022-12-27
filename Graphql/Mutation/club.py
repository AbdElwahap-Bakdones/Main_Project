from ..TypingObject import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from abc import ABC, abstractmethod, abstractclassmethod
from django.http import HttpResponse
from .. import QueryStructure


class AddClubInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    location = graphene.String(required=True)
    is_available = graphene.Boolean(required=True)


class InputUpdateClub(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String(required=True)
    is_available = graphene.Boolean(required=True)


class AddClub  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.Field(typeobject.ClubObjectType)

    class Arguments:
        ClubData = AddClubInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_club", user):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            # get manager_id
            manager_id = models.Manager.objects.get(user_id=user).pk
            # add manager_id to data
            kwargs["ClubData"].update({"manager_id": manager_id})
            seria = serializer.ClubSerializer(data=kwargs["ClubData"])
            if seria.is_valid():
                seria.validated_data
                msg = seria.errors
                status = status_code.HTTP_201_CREATED
                club = seria.save()
            else:
                msg = seria.errors
                club = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
            return QueryStructure.MyReturn(self, club, msg, status)
        except Exception as e:
            print('Error in AddClub :')
            print(e)
            return QueryStructure.MyReturn(self, None, 'Some thing wrong1', status_code.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateClub(graphene.Mutation):
    club = graphene.Field(typeobject.ClubObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        ClubData = InputUpdateClub()

    @classmethod
    def mutate(self, root, info, id, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_club", user):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            sub = models.Club.objects.get(id=id)
            seria = serializer.ClubSerializer(sub,
                                              data=kwargs, partial=True)
            if seria.is_valid():
                seria.validated_data
                msg = seria.errors
                status = status_code.HTTP_200_OK
                club = seria.save()
            else:
                msg = seria.errors
                club = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
            return QueryStructure.MyReturn(self, club, msg, status)
        except Exception as e:
            print('Error in UpdateClub')
            print(e)
            return QueryStructure.MyReturn(self, None, 'Some thing wrong1', status_code.HTTP_500_INTERNAL_SERVER_ERROR)
