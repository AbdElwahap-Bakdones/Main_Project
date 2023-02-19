from core.models import Team, Team_members
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class SearchMyTeamByName(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.TeamConnection, name=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team'):
            return QueryFields.rise_error(user)
        teams_id = Team_members.objects.filter(
            player_id__user_id=user, team_id__name=kwargs['name'], is_leave=False).values_list('team_id_id', flat=True)
        data = Team.objects.filter(
            pk__in=teams_id, deleted=False)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


class SearchTeamByName(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.TeamConnection, name=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team'):
            return QueryFields.rise_error(user)
        data = Team.objects.filter(
            name=kwargs['name'], deleted=False)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


class MyAllTeam(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.TeamConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team_members'):
            return QueryFields.rise_error(user)
        teams_id = Team_members.objects.filter(
            player_id__user_id=user, is_leave=False).values_list('team_id_id', flat=True)
        data = Team.objects.filter(pk__in=teams_id)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


class GetTeamById(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.TeamConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_team_members'):
            return QueryFields.rise_error(user)
        team_id = Team_members.objects.filter(
            player_id__user_id=user, team_id__id=kwargs['id'], is_leave=False).get().team_id.pk
        data = Team.objects.filter(pk=team_id, deleted=False)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)
