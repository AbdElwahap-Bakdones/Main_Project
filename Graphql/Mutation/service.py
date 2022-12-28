from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure


class AddService(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.ServiceObjectType)

    class Arguments:
        ServiceData = inputtype.AddServiceInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        # checkPermission("core.add_service", info)
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_stadium", user):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)

            seria = serializer.ServiceSerializer(
                data=kwargs["ServiceData"])
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
