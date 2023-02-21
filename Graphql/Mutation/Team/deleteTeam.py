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
            if not checkPermission("core.change_team", user):
                return QueryStructure.NoPermission(self)

            can_delete = DeleteTeam.__can_delete(team_id=team_id, user=user)
            if not can_delete['state']:
                return QueryStructure.BadRequest(self, message=can_delete['error'])
            team = can_delete['team']
            team.update(deleted=True)
            models.Team_members.objects.filter(
                team_id=team.get().pk, is_leave=False).update(is_leave=True)
            return QueryStructure.OK(self, data=team.get())
        except Exception as e:
            print('Error in CreateTeam !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))

    def __can_delete(team_id: int, user: models.User) -> dict:
        is_captin = models.Team_members.objects.filter(
            player_id__user_id=user, team_id=team_id, is_captin=True)
        if not is_captin.exists():
            return {'state': False, 'error': 'onlay admin can delete !'}
        team = models.Team.objects.filter(pk=team_id, deleted=False)
        if not team.exists():
            return {'state': False, 'error': 'id team not found !'}
        if team.get().search_game:
            return {'state': False, 'error': 'team has event \'search Game\' !'}

        return {'state': True, 'team': team}
