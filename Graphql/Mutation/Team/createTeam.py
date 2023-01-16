from ...ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ...Auth.permission import checkPermission
from rest_framework import status as status_code
from ... import QueryStructure


class CreateTeam(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.TeamObjectType)

    class Arguments:
        data = inputtype.AddTeamInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_team", user):
                return QueryStructure.NoPermission(self)
            # member_seria =serializer.
            print(kwargs)
            return QueryStructure.OK(self)
        except Exception as e:
            print('Error inCreateTeam !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))
