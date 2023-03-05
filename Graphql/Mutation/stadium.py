from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from django.db.models import Q
from ..Auth.permission import checkPermission
from .. import QueryStructure
from rest_framework import status as status_code
from datetime import datetime


class AddStadium(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.StadiumObjectType)

    class Arguments:
        data = inputtype.AddStadiumInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_stadium", user):
                return QueryStructure.NoPermission(self)
            data = kwargs["data"]
            club = models.Club.objects.filter(
                id=data['club_id'], manager_id__user_id=user)
            section_obj = models.Section.objects.filter(club_id=club.get(),
                                                        id=data["section_id"], is_deleted=False)
            if not section_obj.exists():
                return QueryStructure.BadRequest(self, message="the section or club not found")
            seria = serializer.StadiumSerializer(
                data=data)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                club.update(number_stad=club.get().number_stad+1)
                return QueryStructure.Created(self, data=data)
            else:
                print('serializer Errors in AddStadium')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in AddStadium')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))


class UpdateStadium(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.StadiumObjectType)

    class Arguments:
        data = inputtype.UpdateStadiumInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_stadium", user):
                return QueryStructure.NoPermission(self)
            # if checkPermission("core.add_club", user):
            #     userType = "manager"
            # userType = "subManager"
            # if userType == "subManager":
            #     sub = models.Stadium.objects.filter(
            #         id=data["id"], section_id__sub_manager_id__user_id=user, is_deleted=False)
            # else:
            #     sub = models.Stadium.objects.filter(
            #         id=data["id"], section_id__club_id__manager_id__user_id=user, is_deleted=False)
            # if not sub.exists():
            #     return QueryStructure.NotFound(self)
            data = kwargs['data']
            print(data)
            stad_obj = models.Stadium.objects.filter(Q(id=data["id"]) & Q(is_deleted=False) & (
                                                     Q(section_id__sub_manager_id__user_id=user) | Q(section_id__club_id__manager_id__user_id=user)))

            if not stad_obj.exists():
                return QueryStructure.BadRequest(instanse=self, message='Stadium id not found')
            seria = serializer.StadiumSerializer(stad_obj.first(),
                                                 data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Updated(self, data=data)
            else:
                print('serializer Errors in UpdateStadium')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in UpdateStadium')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))


class DeleteStadium(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.StadiumObjectType)

    class Arguments:
        data = inputtype.DeleteStadiumInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.delete_stadium", user.pk):
                return QueryStructure.NoPermission(self)
            data = kwargs['data']
            sub = models.Stadium.objects.filter(section_id__club_id__manager_id__user_id=user.pk,
                                                pk=data["id"], is_deleted=False)
            if not sub.exists():
                return QueryStructure.BadRequest(instanse=self, message='Stadium Id not foun or stadium alrady deleted !')
            reservation = models.Reservation.objects.filter(
                duration_id__stad_id=sub.first(), duration_id__end_time__gt=datetime.now().time(), date__gt=datetime.now().date(), canceled=False)
            if reservation.exists():
                return QueryStructure.BadRequest(self, message='You cannot delete existing reservations')
            data.update({"is_deleted": True})
            seria = serializer.StadiumSerializer(
                sub.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Deleted(self, data=data)
            else:
                print('serializer Errors in DeleteStadium')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in DeleteStadium')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))
