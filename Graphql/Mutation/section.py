from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure

# def checkmyclub(idClub: id, self: object, info: object):
#     myclub = models.Club.objects.filter(manager_id=models.Manager.objects.get(
#         user_id=info.context.META["user"])).first()
#     if not myclub:
#         return self(Section=None, message="this not your club", status=401)


class AddSection(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.SectionObjectType)

    class Arguments:
        SectionData = inputtype.AddSectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_section", user):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            seria = serializer.SectionSerializer(
                data=kwargs["SectionData"])
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
            msg = e
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)


class UpdatSection(graphene.Mutation):
    section = graphene.Field(typeobject.SectionObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        sub_manager_id = graphene.ID()
        is_available = graphene.Boolean()

    @classmethod
    def mutate(self, root, info, id, **kwargs):
        checkPermission("core.change_section", info)
        sub = models.Section.objects.get(id=id)
        seria = serializer.SectionSerializer(sub,
                                             data=kwargs, partial=True)
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            section = seria.save()
        else:
            msg = seria.errors
            section = None
            status = 400
        return self(section=section, message=msg, status=status)
