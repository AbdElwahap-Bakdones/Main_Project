from graphene_django.rest_framework.mutation import SerializerMutation
from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure
from abc import ABC, abstractmethod, abstractclassmethod
from django.http import HttpResponse


class AddSection  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.Field(typeobject.SectionObjectType)

    class Arguments:
        SectionData = inputtype.AddSectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_section", user):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            seria = serializer.SectionSerializer(data=kwargs["SectionData"])
            if seria.is_valid():
                seria.validated_data
                msg = seria.errors
                status = status_code.HTTP_201_CREATED
                data = seria.save()
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


class UpdateSection(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.SectionObjectType)

    class Arguments:
        SectionData = inputtype.UpdateSectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.change_section", user.pk):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            data = kwargs['SectionData']
            Section_object = models.Section.objects.filter(
                pk=data['id'], is_deleted=False)
            if not Section_object.exists():
                msg = 'there is no Section with id='+data['id']
                data = None
                status = status_code.HTTP_404_NOT_FOUND
                return QueryStructure.MyReturn(self, None, msg, status)

            seria = serializer.SectionSerializer(
                Section_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                msg = 'updated!'
                status = status_code.HTTP_200_OK
                data = seria.save()
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
        SectionData = inputtype.DeleteSectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.delete_section", user.pk):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            data = kwargs['SectionData']
            Section_object = models.Section.objects.filter(
                pk=data["id"], is_deleted=False)
            if not Section_object.exists():
                msg = 'there is no Section with id='+data['id']
                Section = None
                status = status_code.HTTP_404_NOT_FOUND
                return QueryStructure.MyReturn(self, None, msg, status)

            data.update({"is_deleted": True})
            seria = serializer.SectionSerializer(
                Section_object.first(), data=data, partial=True)
            if seria.is_valid():
                seria.validated_data
                msg = 'deleted!'
                status = status_code.HTTP_200_OK
                Section = seria.save()
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
