from core import models, serializer
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene
from django.db.models import Subquery, Value
from django.db import models as MODELS


class AllStadiumByType(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, type_id=graphene.ID(required=True), available=graphene.Boolean(required=True))

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_stadium'):
            return QueryFields.rise_error(user)
        data = models.Stadium.objects.filter(
            type_id__id=kwargs['type_id'], is_deleted=False, is_available=kwargs['available'])
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


class GetStadiumByIdClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, club_id=graphene.ID(required=True), available=graphene.Boolean(required=True))

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_stadium'):
            return QueryFields.rise_error(user)
        data = models.Stadium.objects.filter(
            section_id__club_id__id=kwargs['club_id'], is_deleted=False, is_available=kwargs['available'])
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


class GetStadium(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.change_stadium'):
            return QueryFields.rise_error(user)
        if QueryFields.user_type(user, models.Manager):
            data = models.Stadium.objects.filter(section_id__club_id__manager_id__user_id=user, section_id__is_deleted=False,
                                                 section_id__club_id__is_deleted=False, pk=kwargs['id'], is_deleted=False)
        elif QueryFields.user_type(user, models.SubManager):
            data = models.Stadium.objects.filter(section_id__sub_manager_id__user_id=user, section_id__is_deleted=False,
                                                 section_id__club_id__is_deleted=False, pk=kwargs['id'], is_deleted=False)
        else:
            return QueryFields.NoPermission_403(info=info)
        if data.exists():
            return QueryFields.OK(info=info, data=data)
        return QueryFields.NotFound(info=info)


class GetStadiumBySection(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, section_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.change_club'):
            return QueryFields.rise_error(user)
        data = models.Stadium.objects.filter(section_id__club_id__manager_id__user_id=user, section_id__club_id__is_deleted=False,
                                             section_id__is_deleted=False, section_id__id=kwargs['section_id'], is_deleted=False)
        if not data.exists():
            QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


class StadiumFilter(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.StadiumConnection, id=graphene.ID(), club_id=graphene.ID(), type_id=graphene.ID(), is_available=graphene.Boolean(), has_legua=graphene.Boolean())

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_stadium'):
            return QueryFields.rise_error(user)
        if kwargs.__len__() == 0:
            return QueryFields.queryAll(models.Stadium, info=info)
        data = queryByFilter(kwargs)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


def queryByFilter(kwargs: object) -> models.Stadium.objects.filter:
    if 'club_id' in kwargs:
        kwargs['section_id__club_id'] = kwargs['club_id']
        del kwargs['club_id']
    data = models.Stadium.objects.filter(**kwargs)
    return data
