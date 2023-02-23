from core import models, serializer


class MemmberClass():
    def __init__(self, user: models.User, team_id: int, memmbers: list = []):
        print('int MemmberClass')
        self.user = user
        self.memmbers = memmbers
        self.team_id = team_id
        self.errors = 'ok'
        self.is_captin = False

    def __add_error_message(self, message: str):
        if self.errors == 'ok':
            self.errors = message
            return
        self.errors = self.errors+' \n' + message
        return

    def __run_validate_fun(self, fun):
        try:
            for f in fun:
                if not f[0](**f[1]):
                    return False
            return True
        except Exception as e:
            print('error in MemmberClass.__run_validate_fun')
            print(str(e))
            self.__add_error_message(str(e))
            return False

    def __is_request_removeMemmber_valid(self) -> bool:
        functions = [
            (self.__is_team_exists, {}),
            (self.__is_captin, {}),
            (self.__is_players_exists, {}),
            (self.__is_player_in_team, {}),
            (self.__is_caption_inMemmbers, {})
        ]
        return self.__run_validate_fun(functions)

    def __is_request_leaveTeam_valid(self) -> bool:
        functions = [
            (self.__is_team_exists, {}),
            (self.__is_captin, dict(throw_exception=False)),
            (self.__is_user_inTeam, {})
        ]
        return self.__run_validate_fun(functions)

    def __is_request_addMemmber_valid(self) -> bool:
        functions = [
            (self.__is_team_exists, {}),
            (self.__is_captin, {}),
            (self.__is_players_exists, {}),
            (self.__is_player_not_in_team, {}),
            (self.__is_friend, {})
        ]
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

    def __is_player_not_in_team(self) -> bool:
        memmber_objcs = models.Team_members.objects.filter(
            team_id=self.team_id, player_id__in=self.players.values_list('pk', flat=True), is_leave=False)
        if not memmber_objcs.exists():
            self.memmbers_objecs = memmber_objcs
            return True
        self.__add_error_message(' one or more player alrady in team')
        return False

    def __is_player_in_team(self) -> bool:
        memmber_objcs = models.Team_members.objects.filter(
            team_id=self.team_id, player_id__in=self.players.values_list('pk', flat=True), is_leave=False)
        if memmber_objcs.count() == self.players.count():
            self.memmbers_objecs = memmber_objcs
            return True
        self.__add_error_message(' one or more player not in team')
        return False

    def __is_friend(self) -> bool:
        friend = models.Friend.objects.filter(
            player1__user_id=self.user, player2__in=self.players.values_list('pk', flat=True), state='accepted')
        if self.memmbers.__len__() == friend.__len__():
            return True
        self.__add_error_message('one or more memmber not friend ! ')
        return False

    def __is_captin(self, throw_exception: bool = True) -> bool:
        caption = models.Team_members.objects.filter(
            team_id=self.team_id, is_captin=True, player_id__user_id=self.user)
        if throw_exception and not caption.exists():
            self.__add_error_message('Only admin can do this operation ! ')
            return False
        if caption.exists():
            self.is_captin = True
            self.captin_obj = caption
        return True

    def __is_user_inTeam(self) -> bool:
        memmber = models.Team_members.objects.filter(
            player_id__user_id=self.user, is_leave=False, team_id=self.team_id)
        if memmber.exists():
            self.memmbers_objecs = memmber
            return True
        self.__add_error_message(
            'Team does not exist or you have already left')
        return False

    def __is_caption_inMemmbers(self) -> bool:
        cond = self.memmbers_objecs.filter(
            player_id=self.captin_obj.get().player_id)
        if cond.exists():
            self.__add_error_message(
                'can\'t remove caption but you can delete Team ')
            return False
        return True

    def __serializer_member(self, player) -> bool:
        data = {'player_id': player.pk, 'team_id': self.team.get().pk}
        seria = serializer.MembersTeamSerializer(data=data)
        if not seria.is_valid():
            print(seria.errors)
            self.__add_error_message(seria.errors)
            return False
        seria.save()
        return True

    def add_memmber(self) -> bool:
        try:
            if self.__is_request_addMemmber_valid() and sum(list(map(self.__serializer_member, self.players))):
                memmbers_count = models.Team_members.objects.filter(
                    team_id=self.team_id, is_leave=False).count()
                self.team.update(member_count=memmbers_count)
                return True
            return False
        except Exception as e:
            print('Erro in MemmberClass.add_memmber')
            print(e)
            self.__add_error_message(str(e))
            return False

    def remove_memmber(self) -> bool:
        try:
            if self.__is_request_removeMemmber_valid():
                self.memmbers_objecs.update(is_leave=True)
                memmbers_count = models.Team_members.objects.filter(
                    team_id=self.team_id, is_leave=False).count()
                self.team.update(member_count=memmbers_count)
                return True
            return False
        except Exception as e:
            print('Erro in MemmberClass.remove_memmber')
            print(e)
            self.__add_error_message(str(e))
            return False

    def leave_team(self) -> bool:
        try:
            if self.__is_request_leaveTeam_valid():
                if self.is_captin:
                    self.team.update(deleted=True)
                    self.team = models.Team.objects.filter(pk=self.team_id)
                    return True

                self.memmbers_objecs.update(is_leave=True)
                memmbers_count = models.Team_members.objects.filter(
                    team_id=self.team_id, is_leave=False).count()
                self.team.update(member_count=memmbers_count)
                return True
            return False
        except Exception as e:
            print('Erro in MemmberClass.leave_team')
            print(e)
            self.__add_error_message(str(e))
            return False
