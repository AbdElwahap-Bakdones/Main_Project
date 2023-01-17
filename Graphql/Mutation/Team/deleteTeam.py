from ...ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ...Auth.permission import checkPermission
from ... import QueryStructure


class DeleteTeam(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.TeamObjectType)

    class Arguments:
        data = inputtype.DeleteTeamInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            team_id = kwargs['data']['pk']
            is_captin = models.Team_members.objects.filter(player_id__user_id=user, team_id=team_id, is_captin=True)
            if not checkPermission("core.change_team", user) or not is_captin.exists():
                return QueryStructure.NoPermission(self)

            team = models.Team.objects.filter(pk=team_id)
            can_delete = DeleteTeam.__can_delete(team.get())
            if not can_delete['state']:
                return QueryStructure.BadRequest(self, message=can_delete['error'])
            team.update(deleted=True)
            return QueryStructure.OK(self, data=team.get())
        except Exception as e:
            print('Error in CreateTeam !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))

    def __can_delete(team: models.Team) -> dict:
        if team.deleted:
            return {'state': False, 'error': 'alrady deleted !'}
        if team.search_game:
            return {'state': False, 'error': 'team has event \'search Game\' !'}
        return {'state': True}
