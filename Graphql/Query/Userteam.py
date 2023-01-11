from core.models import Team_members
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class AllTeamMembers(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.Team_membersConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team_members'):
            return QueryFields.rise_error(user)
        data = Team_members.objects.filter(
            player_id__user_id=user, is_leave=False)
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
