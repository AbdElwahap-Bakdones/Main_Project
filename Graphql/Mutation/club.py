from ..TypingObject import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission


class ClubInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    number_stad = graphene.Int(required=True)
    location = graphene.String(required=True)
    is_available = graphene.Boolean(required=True)


class AddClub(graphene.Mutation):
    club = graphene.Field(typeobject.ClubObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        ClubData = ClubInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        checkPermission("core.add_club", info)
        kwargs["ClubData"].update({"manager_id": models.Manager.objects.get(
            user_id=info.context.META["user"]).pk})
        seria = serializer.ClubSerializer(
            data=kwargs["ClubData"])
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            club = seria.save()
        else:
            msg = seria.errors
            club = None
            status = 400
        return self(club=club, message=msg, status=status)


class UpdateClub(graphene.Mutation):
    club = graphene.Field(typeobject.ClubObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        manager_id = graphene.ID()
        number_stad = graphene.Int()
        location = graphene.String()
        is_available = graphene.Boolean()

    @classmethod
    def mutate(self, root, info, id, **kwargs):
        checkPermission("core.change_club", info)
        sub = models.Club.objects.get(id=id)
        seria = serializer.ClubSerializer(sub,
                                          data=kwargs, partial=True)
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            club = seria.save()
        else:
            msg = seria.errors
            club = None
            status = 400
        return self(club=club, message=msg, status=status)
