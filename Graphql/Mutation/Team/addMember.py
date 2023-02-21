from ...ModelsGraphQL import typeobject, inputtype
import graphene
from ...Auth.permission import checkPermission
from ... import QueryStructure
from .Memmber import MemmberClass


class AddMember(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.TeamObjectType)

    class Arguments:
        data = inputtype.AddMembersInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            team_id = kwargs['data']['team_pk']
            members = kwargs['data']['members']
            if not checkPermission("core.add_team_members", user):
                return QueryStructure.NoPermission(self)
            class_obj = MemmberClass(user, team_id, members)
            if class_obj.add_memmber():
                return QueryStructure.Created(instanse=self, data=class_obj.team.get())
            return QueryStructure.BadRequest(instanse=self, message=class_obj.errors)
        except Exception as e:
            print('Error AddMember !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))

    # def __save_serializer(self, seria):
    #     return seria.save()
