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
            if not checkPermission("core.add_team_members", user):
                return QueryStructure.NoPermission(self)
            class_obj = AddMemmberClass(user, team_id, members)
            if class_obj.add_memmber():
                return QueryStructure.Created(instanse=self, data=class_obj.team.get())

            return QueryStructure.BadRequest(instanse=self, message=class_obj.errors)
        except Exception as e:
            print('Error AddMember !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))


class AddMemmberClass():
    def __init__(self, user: models.User, team_id: int, memmbers: list):
        self.user = user
        self.memmbers = memmbers
        self.team_id = team_id
        self.errors = 'ok'

    def __add_error_message(self, message: str):
        if self.errors == 'ok':
            self.errors = message
            return
        self.errors = self.errors+' \n' + message
        return

    def __run_validate_fun(self, *fun):
        for f in fun[0]:
            if not f():
                return False
        return True

    def __is_request_valid(self) -> bool:
        functions = [
            self.__is_team_exists,
            self.__is_captin,
            self.__is_players_exists,
            self.__is_player_in_team,
            self.__is_friend]
        return self.__run_validate_fun(functions)

    def __is_team_exists(self) -> bool:
        team = models.Team.objects.filter(id=self.team_id, deleted=False)
        if team.exists():
            self.team = team
            return True
        self.__add_error_message('team id not exists')
        return False

    def __is_players_exists(self) -> bool:
        players = models.Player.objects.filter(pk__in=self.memmbers)
        if players.__len__() == self.memmbers.__len__():
            self.players = players
            return True
        self.__add_error_message(' one or more player id not exists')
        return False

    def __is_player_in_team(self) -> bool:
        if not models.Team_members.objects.filter(team_id=self.team_id, player_id__in=self.players.values_list('pk', flat=True), is_leave=False).exists():
            return True
        self.__add_error_message(' one or more player alrady in team')
        return False

    def __is_friend(self) -> bool:
        friend = models.Friend.objects.filter(
            player1__user_id=self.user, player2__in=self.players.values_list('pk', flat=True), state='accepted')
        if self.memmbers.__len__() == friend.__len__():
            return True
        self.__add_error_message('one or more memmber not friend ! ')
        return False

    def __is_captin(self) -> bool:
        caption = models.Team_members.objects.filter(
            team_id=self.team_id, is_captin=True, player_id__user_id=self.user)
        if caption.exists():
            return True
        self.__add_error_message('only admin can add memmber ! ')
        return False

    def add_memmber(self) -> bool:
        if self.__is_request_valid() and sum(list(map(self.__serializer_member, self.players))):
            return True
        return False

    def __serializer_member(self, player) -> bool:
        data = {'player_id': player.pk, 'team_id': self.team.get().pk}
        seria = serializer.MembersTeamSerializer(data=data)
        if not seria.is_valid():
            print(seria.errors)
            self.__add_error_message(seria.errors)
            return False
        seria.save()
        member_count = self.team.get().member_count
        self.team.update(member_count=member_count+1)
        return True

    # def __save_serializer(self, seria):
    #     return seria.save()
