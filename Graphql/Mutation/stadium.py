from ..ModelsGraphQL import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission


class StadiumInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    section_id = graphene.ID(required=True)
    type_id = graphene.ID(required=True)
    size = graphene.Float(required=True)
    is_available = graphene.Boolean(required=True)
    has_legua = graphene.Boolean(required=True)


class AddStadium(graphene.Mutation):
    stadium = graphene.Field(typeobject.StadiumObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        StadiumData = StadiumInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        checkPermission("core.add_stadium", info)
        seria = serializer.StadiumSerializer(
            data=kwargs["StadiumData"])
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
