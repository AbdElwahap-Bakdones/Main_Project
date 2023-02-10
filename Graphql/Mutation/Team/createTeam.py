from ...ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ...Auth.permission import checkPermission
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
            team = CreateTeam.create_team(kwargs['data'])
            if not team['state']:
                return QueryStructure.BadRequest(self, message=team['errors'])

            admin_data = {'player_id': models.Player.objects.get(
                user_id=user).pk, 'team_id': team['team'].pk, 'is_captin': True}
            member = CreateTeam.add_admin(admin_data)

            if not member['state']:
                models.Team.objects.filter(
                    pk=team['team'].pk).update(deleted=True)

                return QueryStructure.BadRequest(self, message=member['errors'])

            return QueryStructure.Created(self, data=team['team'])

        except Exception as e:
            print('Error inCreateTeam !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))

    def create_team(data: dict) -> dict:
        team_seria = serializer.TeamSerializer(data=data)
        if team_seria.is_valid():
            team = team_seria.save()
            return {'state': True, 'team': team}
        return {'state': False, 'errors': team_seria.errors}

    def add_admin(data: dict) -> dict:
        member_seria = serializer.MembersTeamSerializer(data=data)
        if member_seria.is_valid():
            member = member_seria.save()
            return {'state': True, 'team': member}
        return {'state': False, 'errors': member_seria.errors}
