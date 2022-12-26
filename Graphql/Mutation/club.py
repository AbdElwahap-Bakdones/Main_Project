from ..TypingObject import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from rest_framework import status as status_code


class ClubInput(graphene.InputObjectType):
    name = graphene.String(required=True)
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
        user = info.context.META["user"]
        if not checkPermission("core.add_club", user):
            return self(club=None, message='You do not have permission to complete the process', status=status_code.HTTP_401_UNAUTHORIZED)
        manager_id = models.Manager.objects.get(user_id=user).pk
        print(kwargs)
        kwargs["ClubData"].update({"manager_id": manager_id})
        seria = serializer.ClubSerializer(data=kwargs["ClubData"])
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = status_code.HTTP_201_CREATED
            club = seria.save()
        else:
            msg = seria.errors
            club = None
            status = status_code.HTTP_406_NOT_ACCEPTABLE
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
