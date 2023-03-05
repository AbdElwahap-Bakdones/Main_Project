from graphene_django.rest_framework.mutation import SerializerMutation
from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure
from datetime import datetime


class AddSection  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.Field(typeobject.SectionObjectType)

    class Arguments:
        data = inputtype.AddSectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_section", user):
                return QueryStructure.NoPermission(self)
            sub_manager_obj = None
            is_there_sub_manager = False
            club_obj = models.Club.objects.filter(
                pk=kwargs['data']['club_id'], manager_id__user_id=user)
            if not club_obj.filter().exists():
                return QueryStructure.BadRequest(self, message='Club id not found')

            if 'sub_manager_id' in kwargs['data']:
                is_there_sub_manager = True
                sub_manager_obj = models.SubManager.objects.filter(
                    club_id=club_obj.get())
            if is_there_sub_manager and not sub_manager_obj.exists():
                return QueryStructure.BadRequest(self, message='Sub Manager id not found')
            seria = serializer.SectionSerializer(data=kwargs["data"])
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Created(instanse=self, data=data)
            else:
                print('serializer Errors in AddSection')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in AddSection')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))

        # if not models.SubManager.objects.filter(
        #         pk=kwargs['data']['sub_manager_id'],
        #         club_id=kwargs['data']['club_id'],
        #         club_id__manager_id__user_id=user).exists():
        #     return QueryStructure.BadRequest(self, message='maybe club id or sub manager not found')


class UpdateSection(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.SectionObjectType)

    class Arguments:
        data = inputtype.UpdateSectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.change_section", user.pk):
                return QueryStructure.NoPermission(self)
            data = kwargs['data']
            Section_object = models.Section.objects.filter(
                pk=data['id'], club_id__manager_id__user_id=user.pk, is_deleted=False)
            if not Section_object.exists():
                return QueryStructure.BadRequest(self, message='section not found')
            seria = serializer.SectionSerializer(
                Section_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Updated(self, data=data)
            else:
                print('serializer Errors in UpdateSection')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in UpdateSection')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))


class DeleteSection(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.SectionObjectType)

    class Arguments:
        data = inputtype.DeleteSectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.delete_section", user.pk):
                return QueryStructure.NoPermission(self)
            data = kwargs['data']
            Section_object = models.Section.objects.filter(pk=data['id'],
                                                           club_id__manager_id__user_id=user.pk,  is_deleted=False)
            if not Section_object.exists():
                return QueryStructure.BadRequest(self, message='section not found')
            reservation = models.Reservation.objects.filter(
                duration_id__stad_id__section_id=Section_object.first(), duration_id__end_time__gt=datetime.now().time(), date__gt=datetime.now().date(), canceled=False)
            if reservation.exists():
                return QueryStructure.BadRequest(self, message='You cannot delete existing reservations')
            data.update({"is_deleted": True})
            seria = serializer.SectionSerializer(
                Section_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Deleted(self, data=data)
            else:
                print('serializer Errors in DeleteSection')
                print(seria.errors)
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.BadRequest(instanse=self)
        except Exception as e:
            print('Error in DeleteSection')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))
