from core import models
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
from django.db.models import Q
from datetime import datetime
import graphene


class DurationByStadium(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.DurationConnection, stadium=graphene.ID(required=True), date=graphene.Date(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_reservation'):
                return QueryFields.rise_error(user)
            duration = models.Duration.objects.filter(
                stad_id=kwargs['stadium'], is_deleted=False, is_available=True)
            reservation = models.Reservation.objects.filter(
                date=kwargs['date'], duration_id__in=duration.values_list('pk', flat=True))
            avlaible_duration = duration.filter(
                ~Q(pk__in=reservation.values_list('duration_id', flat=True)))
            if avlaible_duration.count()>0:
                return QueryFields.OK(info=info, data=avlaible_duration)
            return QueryFields.NotFound(info=info, msg='Sorry the date you have chosen is complete')
        except Exception as e:
            print('Error in DurationByStadium')
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
        if QueryFields.user_type(user, Manager):

            data = models.Duration.objects.filter(stad_id__section_id__club_id__manager_id__user_id=user,
                                                  pk=kwargs['id'])
        else:
            data = models.Duration.objects.filter(stad_id__section_id__sub_manager_id__user_id=user,
                                                  pk=kwargs['id'])
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)
