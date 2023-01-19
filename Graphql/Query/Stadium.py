from core.models import Stadium, Duration,Manager,SubManager
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene
from django.db.models import Q

# manager or sub manager show all your stadium example :in selector add duration
class AllStadium(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, club_id=graphene.ID(required=True))
    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not Manager.objects.filter(user_id=user).exists() or SubManager.objects.filter(user_id=user).exists():
            return QueryFields.BadRequest(info=info)
        data = Stadium.objects.filter(Q(section_id__club_id__user_id=user)or Q(sub_manager_id=user),
            section_id__club_id__id=kwargs['club_id'], is_deleted=False, is_available=True)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info,data=data)

# player search on stadium by type or size
class GetStadiumByTypeOrSize(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, club_id=graphene.ID(required=True), type_id=graphene.ID(), size=graphene.Int())
    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_stadium'):
            return QueryFields.rise_error(user)
        data = queryByFilter(kwargs)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info,data=data)


def queryByFilter(kwargs: object) -> Stadium.objects.filter:
    if 'type_id' in kwargs and 'size' in kwargs:
        data = Stadium.objects.filter(
            size=kwargs['size'], type_id__id=kwargs['type_id'], section_id__club_id__id=kwargs['club_id'], is_deleted=False, is_available=True)
    elif 'type_id' in kwargs and not('size' in kwargs):
        data = Stadium.objects.filter(
            type_id__id=kwargs['type_id'], section_id__club_id__id=kwargs['club_id'], is_deleted=False, is_available=True)
    elif not('type_id' in kwargs) and 'size' in kwargs:
        data = Stadium.objects.filter(
            size=kwargs['size'], section_id__club_id__id=kwargs['club_id'], is_deleted=False, is_available=True)
    else:
        data = Stadium.objects.filter(
            section_id__club_id__id=kwargs['club_id'], is_deleted=False, is_available=True)
    return data
