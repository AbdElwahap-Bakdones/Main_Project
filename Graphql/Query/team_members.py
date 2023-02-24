from core.models import Team, Team_members
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class MembersTeamById(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.Team_membersConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        team_id = kwargs['id']
        if not QueryFields.is_valide(info, user, 'core.view_team_members'):
            return QueryFields.rise_error(user)
        is_user_memmber = Team_members.objects.filter(
            player_id__user_id=user, team_id=team_id, is_leave=False)

        if not is_user_memmber.exists():
            return QueryFields.NotFound(info=info, msg='team id not exisits or you not in the team !')
        data = Team_members.objects.filter(team_id=team_id, is_leave=False)
        return QueryFields.OK(info=info, data=data)


# class GetMemmberById(ObjectType, QueryFields):
#     data = relay.ConnectionField(
#         relays.Team_membersConnection, team_id=graphene.ID(required=True),
#         player_id=graphene.ID(required=True))

#     def resolve_data(root, info, **kwargs):
#         user = info.context.META['user']
#         team_id = kwargs['team_id']
#         player_id = kwargs['player_id']
#         if not QueryFields.is_valide(info, user, 'core.view_team_members'):
#             return QueryFields.rise_error(user)
#         is_user_memmber = Team_members.objects.filter(
#             player_id__user_id=user, team_id=team_id, is_leave=False)
#         is_player_in_team = Team_members.objects.filter(
#             team_id=team_id, player_id=player_id, is_leave=False)
#         if is_user_memmber.exists() and is_player_in_team.exists():
#             return QueryFields.OK(info=info, data=is_player_in_team)
#         return QueryFields.NotFound(info=info)
