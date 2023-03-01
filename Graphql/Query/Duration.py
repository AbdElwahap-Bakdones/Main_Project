from rest_framework import status as status_code
from django.db.models import Q, QuerySet, Subquery, Value
from django.db import models as MODELS
from itertools import chain
from datetime import datetime
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from core import models
from ..Relay import relays
import graphene


class AllDurationStadium(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.DurationConnection, stadium_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_duration'):
                return QueryFields.rise_error(user)
            stad = models.Stadium.objects.filter(pk=kwargs['stadium_id'])
            if not stad.exists():
                return QueryFields.BadRequest(info=info, msg='Stadium id not found !')
            duration = models.Duration.objects.filter(
                stad_id=stad.get(), is_deleted=False)
            return QueryFields.OK(info=info, data=duration)
        except Exception as e:
            print('Error in AllDurationStadium')
            print(str(e))
            return QueryFields.ServerError(info, msg=str(e))


class AvailableDurationByStadium(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.DurationConnection, stadium=graphene.ID(required=True), date=graphene.Date(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_reservation'):
                return QueryFields.rise_error(user)
            stad_obj = models.Stadium.objects.filter(pk=kwargs['stadium'])
            if not stad_obj.exists():
                return QueryFields.BadRequest(info=info, msg='staduim id not found')
            duration = models.Duration.objects.filter(
                stad_id=stad_obj.get().pk, is_deleted=False)
            reservation = models.Reservation.objects.filter(
                date=kwargs['date'], duration_id__in=duration.values_list('pk', flat=True))
            avlaible_duration = duration.filter(Q(is_available=True) &
                                                ~Q(pk__in=reservation.values_list('duration_id', flat=True)))
            avlaible_duration_list = avlaible_duration.values_list(
                'pk', flat=True)
            NAV_duration = duration.filter(~Q(pk__in=avlaible_duration_list)).annotate(available=Value(
                False, output_field=MODELS.BooleanField()))
            avlaible_duration = avlaible_duration.annotate(available=Value(
                True, output_field=MODELS.BooleanField()))
            all_duration = list(chain(NAV_duration, avlaible_duration))
            return QueryFields.OK(info=info, data=all_duration)
        except Exception as e:
            print('Error in AvailableDurationByStadium')
            print(str(e))
            return QueryFields.ServerError(info, msg=str(e))


class DurationByGeo(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.DurationConnection, type_id=graphene.ID(required=True), date=graphene.Date(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_reservation'):
                return QueryFields.rise_error(user)
            type_obj = models.Type.objects.filter(id=kwargs['type_id'])
            if not type_obj.exists():
                return QueryFields.BadRequest(info=info, msg='type id not Found')
            # club_id = models.Club.objects.filter(point__=)

        except Exception as e:
            print('Error in DurationByGeo')
            print(str(e))
            return QueryFields.ServerError(info, msg=str(e))


class GetDuration(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.DurationConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_stadium'):
            return QueryFields.rise_error(user)
        if QueryFields.user_type(user, models.Manager):

            data = models.Duration.objects.filter(stad_id__section_id__club_id__manager_id__user_id=user,
                                                  pk=kwargs['id'])
            if not data.exists():
                return QueryFields.NotFound(info=info)
        elif QueryFields.user_type(user, model=models.SubManager):
            data = models.Duration.objects.filter(stad_id__section_id__sub_manager_id__user_id=user,
                                                  pk=kwargs['id'])
            if not data.exists():
                return QueryFields.NotFound(info=info)
        else:
            return QueryFields.BadRequest(info=info)
        return QueryFields.OK(info=info, data=data)


class IsStadHasDuration(ObjectType, QueryFields):
    data = graphene.Boolean(id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        duration = models.Duration.objects.filter(
            stad_id=kwargs['id'], is_available=True, is_deleted=False)
        if duration.exists():
            return QueryFields.OK(info=info, data=True)
        return QueryFields.BadRequest(info=info, data=False)
