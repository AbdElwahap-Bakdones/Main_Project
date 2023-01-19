from core.models import Team, Team_members
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class GetTeamMembers(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.Team_membersConnection, username=graphene.String(required=True),team=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team_members'):
            return QueryFields.rise_error(user)
        if not Team_members.objects.filter(player_id__user_id=user,team_id__id=kwargs["team"], is_leave=False):
            return QueryFields.BadRequest(info=info)
        data = Team_members.objects.filter(team_id__id=kwargs["team"],
            player_id__user_id__username=kwargs['username'], is_leave=False)
        if not data.exists():
           return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info,data=data)


class AllMyTeamMembers(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.Team_membersConnection, id_team=graphene.Field(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team_members'):
            return QueryFields.rise_error(user)
        data = Team_members.objects.filter(
            team_id__id=kwargs['id_team'], team_id__deleted=False)
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
