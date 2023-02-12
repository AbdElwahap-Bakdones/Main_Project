from graphene_django.rest_framework.mutation import SerializerMutation
from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure
from abc import ABC, abstractmethod, abstractclassmethod
from django.http import HttpResponse


class AddClub  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.Field(typeobject.ClubObjectType)

    class Arguments:
        data = inputtype.AddClubInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_club", user):
                return QueryStructure.NoPermission(self)
            # get manager_id
            manager_id = models.Manager.objects.get(user_id=user).pk
            # add manager_id to data
            kwargs["data"].update({"manager_id": manager_id})
            seria = serializer.ClubSerializer(data=kwargs["data"])
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Created(self, data=data)
            else:
                msg = seria.errors
                data = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in AddClub :')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)


class UpdateClub(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.ClubObjectType)

    class Arguments:
        data = inputtype.UpdateClubInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.change_club", user.pk):
                return QueryStructure.NoPermission(self)
            data = kwargs['data']
            # club_object = models.Club.objects.get(
            #     id=data['id'], is_deleted=False)
            club_object = models.Club.objects.filter(user_id=user,
                                                     pk=data['id'], is_deleted=False)
            if not club_object.exists():
                return QueryStructure.NotFound(self)
            seria = serializer.ClubSerializer(
                club_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Updated(self, data=data)
            else:
                msg = seria.errors
                data = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in UpdateClub')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)


class DeleteClub(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.ClubObjectType)

    class Arguments:
        data = inputtype.DeleteClubInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.delete_club", user.pk):
                return QueryStructure.NoPermission(self)
            data = kwargs['data']
            club_object = models.Club.objects.filter(user_id=user,
                                                     pk=data["id"], is_deleted=False)
            if not club_object.exists():
                return QueryStructure.NotFound(self)

            data.update({"is_deleted": True})
            seria = serializer.ClubSerializer(
                club_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Deleted(self, data=data)
            else:
                msg = seria.errors
                data = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in UpdateClub')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)
