from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure


class StadiumServiceInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    service_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)


class AddServicesForStadiums(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.StadiumServiceObjectType)

    class Arguments:
        StadiumServiceData = inputtype.AddStadiumServiceInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_service", user):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)

            seria = serializer.StadiumServiceSerializer(
                data=kwargs["StadiumServiceData"])
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


class ModificationsToStadiumServices(graphene.Mutation):
    stadiumService = graphene.Field(typeobject.StadiumServiceObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        stad_id = graphene.ID(required=True)
        service_id = graphene.ID(required=True)
        is_available = graphene.Boolean()

    @classmethod
    def mutate(self, root, info, **kwargs):
        checkPermission("core.change_stadiumservice", info)
        sub = models.StadiumService.objects.filter(
            stad_id=kwargs["stad_id"], service_id=kwargs["service_id"]).first()
        seria = serializer.StadiumServiceSerializer(sub,
                                                    data=kwargs, partial=True)
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            stadiumService = seria.save()
        else:
            msg = seria.errors
            stadiumService = None
            status = 400
        return self(stadiumService=stadiumService, message=msg, status=status)
