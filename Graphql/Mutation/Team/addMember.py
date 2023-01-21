from ...ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ...Auth.permission import checkPermission
from ... import QueryStructure


class AddMember(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.TeamObjectType)

    class Arguments:
        data = inputtype.AddMembersInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            team_id = kwargs['data']['pk']
            members = kwargs['data']['members']
            is_captin = models.Team_members.objects.filter(player_id__user_id=user, team_id=team_id, is_captin=True)
            if not checkPermission("core.add_team_members", user) or not is_captin.exists():
                return QueryStructure.NoPermission(self)
            team = models.Team.objects.filter(pk=team_id)
            members_object = AddMember.__is_valid(members=members)
            if members_object != None:
                map(lambda item: AddMember.__add_member(member=item, team_id=team.get()), members_object)
                return QueryStructure.OK(instanse=self, data=team.get())
        except:
            pass

    def __is_valid(members: list) -> models.Player.objects.filter:
        player = models.Player.objects.filter(pk__in=members)
        if player.count() == members.count():
            if not models.Team_members.objects.filter(player_id__in=player).exists():
                return player
        return None

    def __add_member(member: int, team: int):
        return serializer.MembersTeamSerializer(data={'player_id': member.get(), 'team_id': team})
