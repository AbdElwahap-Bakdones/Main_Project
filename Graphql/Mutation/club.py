from graphene_django.rest_framework.mutation import SerializerMutation
from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure
from abc import ABC, abstractmethod, abstractclassmethod
from django.http import HttpResponse
from datetime import datetime


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
                print('serializer Errors in AddClub')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in AddClub :')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))


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
            club_object = models.Club.objects.filter(manager_id__user_id=user.pk,
                                                     pk=data['id'], is_deleted=False)
            if not club_object.exists():
                return QueryStructure.BadRequest(self, message='club id not found')
            seria = serializer.ClubSerializer(
                club_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Updated(self, data=data)
            else:
                print('serializer Errors in UpdateClub')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in UpdateClub :')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))


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
            club_object = models.Club.objects.filter(manager_id__user_id=user.pk,
                                                     pk=data["id"], is_deleted=False)
            if not club_object.exists():
                return QueryStructure.BadRequest(self, message='club id not found')
            reservation = models.Reservation.objects.filter(
                duration_id__stad_id__section_id__club_id=club_object.first(), duration_id__end_time__gt=datetime.now().time(), date__gt=datetime.now().date(), canceled=False)
            if reservation.exists():
                return QueryStructure.BadRequest(self, message='You cannot delete existing reservations')
            data.update({"is_deleted": True})
            seria = serializer.ClubSerializer(
                club_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Deleted(self, data=data)
            else:
                print('serializer Errors in UpdateClub')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in UpdateClub')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))
