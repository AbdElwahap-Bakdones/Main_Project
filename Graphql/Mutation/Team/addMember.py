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
            team_id = kwargs['data']['team_pk']
            members = kwargs['data']['members']
            is_captin = models.Team_members.objects.filter(player_id__user_id=user, team_id=team_id, is_captin=True)
            if not checkPermission("core.add_team_members", user) or not is_captin.exists():
                return QueryStructure.NoPermission(self)
            team = models.Team.objects.filter(pk=team_id)
            #chaeck if request valid and return members object or return None
            member_objects = AddMember.__is_request_valid(members=members)
            serializers = sum(map(lambda item: AddMember.__serializer_member(
                member=item.get(), team_id=team.get(), user=user), member_objects))
            if serializers < member_objects.count():
                return QueryStructure.BadRequest(instanse=self)
            return QueryStructure.OK(instanse=self, data=team.get())
        except Exception as e:
            print('Error AddMember !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))

    def __is_request_valid(members: list) -> models.Player.objects.filter:
        player = models.Player.objects.filter(pk__in=members)
        if player.count() == members.count():
            if not models.Team_members.objects.filter(player_id__in=player).exists():
                return player
        return None

    def __serializer_member(member: models.Player, team: int, user: models.User) -> bool:
        if not models.Friend.objects.filter(player1=member, player2__user_id=user, state='accepted').exists():
            return False
        data = {'player_id': member, 'team_id': team}
        seria = serializer.MembersTeamSerializer(data=data)
