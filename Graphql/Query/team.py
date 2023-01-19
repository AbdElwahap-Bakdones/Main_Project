from core.models import Team, Team_members
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class GetTeam(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.TeamConnection, name_team=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team'):
            return QueryFields.rise_error(user)
        data = Team.objects.filter(
            name=kwargs['name_team'], deleted=False)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info,data=data)


class AllMyTeam(ObjectType, QueryFields):
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
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info,data=data)


class GetMyTeam(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.Team_membersConnection, name_team=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team_members'):
            return QueryFields.rise_error(user)
        data = Team_members.objects.filter(
            player_id__user_id=user, team_id__name=kwargs['name_team'], is_leave=False)
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
