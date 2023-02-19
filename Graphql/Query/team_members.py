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
        if is_user_memmber.exists():
            data = Team_members.objects.filter(team_id=team_id, is_leave=False)
            return QueryFields.OK(info=info, data=data)
        return QueryFields.NotFound(info=info)


# class AllMyTeamMembers(ObjectType, QueryFields):
#     data = relay.ConnectionField(
#         relays.Team_membersConnection, id_team=graphene.Field(required=True))

#     def resolve_data(root, info, **kwargs):
#         print(kwargs)
#         user = info.context.META['user']
#         if not QueryFields.is_valide(info, user, 'core.view_team_members'):
#             return QueryFields.rise_error(user)
#         data = Team_members.objects.filter(
#             team_id__id=kwargs['id_team'], team_id__deleted=False)
#         if not data.exists():
#             QueryFields.set_extra_data(
#                 user, status_code.HTTP_404_NOT_FOUND, 'not exists')
#             return []
#         QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
#         return data
