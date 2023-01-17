from core.models import Duration, Reservation
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
from django.db.models import Q
from datetime import datetime
import graphene


class GetAllowDuration(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.DurationConnection, stadium=graphene.ID(required=True), dateTime=graphene.Date(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_reservation'):
            return QueryFields.rise_error(user)
        if datetime.now().date() > kwargs['dateTime']:
            QueryFields.set_extra_data(
                user, status_code.HTTP_406_NOT_ACCEPTABLE, 'You have to choose today is date or a date after today')
            return []
        duration_list = Duration.objects.filter(
            stad_id__id=kwargs['stadium'], is_available=True, is_deleted=False)
        resrv_list = Reservation.objects.filter(time__date=kwargs['dateTime'],
                                                duration_id__in=duration_list.values_list('pk'), canceled=False).values_list('duration_id__pk')
        data = duration_list.filter(~Q(pk__in=resrv_list))
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
