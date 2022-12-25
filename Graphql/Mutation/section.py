from ..TypingObject import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission


# def checkmyclub(idClub: id, self: object, info: object):
#     myclub = models.Club.objects.filter(manager_id=models.Manager.objects.get(
#         user_id=info.context.META["user"])).first()
#     if not myclub:
#         return self(Section=None, message="this not your club", status=401)


class SectionInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    club_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)


class AddSection(graphene.Mutation):
    section = graphene.Field(typeobject.SectionObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        SectionData = SectionInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        checkPermission("core.add_section", info)
        # checkmyclub(kwargs["SectionData"]["club_id"], self, info)
        kwargs["SectionData"].update({"sub_manager_id": models.SubManager.objects.get(
            user_id=info.context.META["user"]).pk})
        seria = serializer.SectionSerializer(
            data=kwargs["SectionData"])
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
