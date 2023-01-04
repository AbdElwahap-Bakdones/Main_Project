from graphene_django.rest_framework.mutation import SerializerMutation
from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from abc import ABC, abstractmethod, abstractclassmethod
from django.http import HttpResponse
from .. import QueryStructure


class AddClub  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.Field(typeobject.ClubObjectType)

    class Arguments:
        ClubData = inputtype.AddClubInput()

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
        except Exception as e:
            print('Error in AddClub :')
            print(e)
            msg = str(e)
            club = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=club, message=msg, code=status)


class UpdateClub(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.ClubObjectType)

    class Arguments:
        data = inputtype.InputUpdateClub()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.change_club", user.pk):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            data = kwargs['data']
            club_object = models.Club.objects.get(
                id=data['id'], is_deleted=False)
            # club_object = models.Club.objects.filter(
            #     pk=data['id'], is_deleted=False)
            # if not club_object.exists():
            #     msg = 'there is no club with id='+data['id']
            #     club = None
            #     status = status_code.HTTP_404_NOT_FOUND
            #     return QueryStructure.MyReturn(self, None, msg, status)

            seria = serializer.ClubSerializer(
                club_object, data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                msg = 'updated!'
                status = status_code.HTTP_200_OK
                club = seria.save()
            else:
                msg = seria.errors
                club = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in UpdateClub')
            print(e)
            msg = str(e)
            club = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=club, message=msg, code=status)
