from ..TypingObject import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission


class StadiumServiceInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    service_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)


class AddServicesForStadiums(graphene.Mutation):
    stadiumService = graphene.Field(typeobject.StadiumServiceObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        StadiumServiceData = StadiumServiceInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        checkPermission("core.add_stadiumservice", info)
        seria = serializer.StadiumServiceSerializer(
            data=kwargs["StadiumServiceData"])
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
