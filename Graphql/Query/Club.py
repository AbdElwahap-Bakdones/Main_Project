from core.models import Club
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from ..Relay import relays
import graphene
from core import models
from django.db.models import Q, Value
from Bank import models as MODELSBANK
from django.db import models as MODELS


class AllClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubConnection, available=graphene.Boolean(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_club'):
                return QueryFields.rise_error(user)
            data = Club.objects.filter(
                is_deleted=False, is_available=kwargs['available'])
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('error in AllClub')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))


class MyClub(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ClubConnection)

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not models.Manager.objects.filter(user_id=user).exists():
                return QueryFields.BadRequest(info=info)
            data = models.Club.objects.filter(
                manager_id__user_id=user.pk, is_deleted=False)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('error in MyClub')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))


class GetClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubProfileConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not models.Manager.objects.filter(user_id=user).exists():
                return QueryFields.BadRequest(info=info)
            data = models.Club.objects.filter(
                manager_id__user_id=user, pk=kwargs['id'], is_deleted=False)
            if not data.exists():
                return QueryFields.NotFound(info=info)
            balance = MODELSBANK.Account.objects.get(
                client_name=""+str(data.first().pk)+"_"+str(2)).client_ammunt
            print(balance)
            data = data.annotate(balance=Value(
                balance, output_field=MODELS.FloatField()))
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('error in GetClub')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))


class searchClubByName(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubConnection, name=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_club'):
                return QueryFields.rise_error(user)
            data = Club.objects.filter(
                name__iexact=kwargs['name'], is_deleted=False)
            if not data.exists():
                return QueryFields.NotFound(info=info)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('error in searchClubByName')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))


class GetClubById(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ClubConnection, club_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_club'):
                return QueryFields.rise_error(user)
            data = Club.objects.filter(
                id=kwargs['club_id'], is_deleted=False)
            if not data.exists():
                return QueryFields.NotFound(info=info)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('error in getClubById')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))
