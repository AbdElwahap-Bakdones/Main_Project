from ..ModelsGraphQL import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission


class ServiceInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class AddService(graphene.Mutation):
    service = graphene.Field(typeobject.ServiceObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        ServiceData = ServiceInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        checkPermission("core.add_service", info)
        seria = serializer.ServiceSerializer(
            data=kwargs["ServiceData"])
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            service = seria.save()
        else:
            msg = seria.errors
            service = None
            status = 400
        return self(service=service, message=msg, status=status)


class UpdateService(graphene.Mutation):
    service = graphene.Field(typeobject.ServiceObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    @classmethod
    def mutate(self, root, info, id, **kwargs):
        checkPermission("core.change_service", info)
        sub = models.Service.objects.get(id=id)
        seria = serializer.ServiceSerializer(sub,
                                             data=kwargs, partial=True)
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            service = seria.save()
        else:
            msg = seria.errors
            service = None
            status = 400
        return self(service=service, message=msg, status=status)
