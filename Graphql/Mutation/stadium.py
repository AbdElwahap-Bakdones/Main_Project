from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code
from .. import QueryStructure


class AddStadium(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.StadiumObjectType)

    class Arguments:
        StadiumData = inputtype.AddStadiumInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_stadium", user):
                return QueryStructure.MyReturn(self, None, 'You do not have permission to complete the process', status_code.HTTP_401_UNAUTHORIZED)
            seria = serializer.StadiumSerializer(
                data=kwargs["StadiumData"])
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


class UpdateStadium(graphene.Mutation):
    stadium = graphene.Field(typeobject.StadiumObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        section_id = graphene.ID()
        type_id = graphene.ID()
        size = graphene.Float()
        is_available = graphene.Boolean()
        has_legua = graphene.Boolean()

    @classmethod
    def mutate(self, root, info, id, **kwargs):
        checkPermission("core.change_stadium", info)
        sub = models.Stadium.objects.get(id=id)
        seria = serializer.StadiumSerializer(sub,
                                             data=kwargs, partial=True)
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            stadium = seria.save()
        else:
            msg = seria.errors
            stadium = None
            status = 400
        return self(stadium=stadium, message=msg, status=status)
