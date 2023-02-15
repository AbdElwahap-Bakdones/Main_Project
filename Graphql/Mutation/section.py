from graphene_django.rest_framework.mutation import SerializerMutation
from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure


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
            if ['sub_manager_id'] in kwargs['data']:
                is_there_sub_manager = True
                sub_manager_obj = models.SubManager.objects.filter(
                    club_id=club_obj)
            if is_there_sub_manager and sub_manager_obj.exists():
                return QueryStructure.BadRequest(self, message='Sub Manager id not found')
            seria = serializer.SectionSerializer(data=kwargs["data"])
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Created(instanse=self, data=data)
            else:
                msg = seria.errors
                data = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in AddSection :')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)

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
                pk=data['id'], club_id=data['club_id'], club_id__manager_id__user_id=user, is_deleted=False)
            if not Section_object.exists():
                QueryStructure.NotFound(self)
            seria = serializer.SectionSerializer(
                Section_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Updated(self, data=data)
            else:
                msg = seria.errors
                data = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in UpdateSection')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)


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
            Section_object = models.Section.objects.filter(club_id__manager_id__user_id=user, club_id=data["club_id"],
                                                           pk=data["id"], is_deleted=False)
            if not Section_object.exists():
                QueryStructure.NotFound(self)
            data.update({"is_deleted": True})
            seria = serializer.SectionSerializer(
                Section_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Deleted(self, data=data)
            else:
                msg = seria.errors
                Section = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in UpdateSection')
            print(e)
            msg = str(e)
            Section = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=Section, message=msg, code=status)
