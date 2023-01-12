from core.models import Duration, Reservation
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
from django.db.models import Q
import graphene


class searchOnReservation(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ReservationConnection, stadium=graphene.ID(required=True), dateTime=graphene.Date(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_reservation'):
            return QueryFields.rise_error(user)
        duration_list = Duration.objects.filter(
            stad_id__id=kwargs['stadium'], is_available=True, is_deleted=False)
        print(duration_list)
        resrv_list = Reservation.objects.filter(time__date=kwargs['dateTime'],
                                                duration_id__in=duration_list.values_list('pk')).values_list('duration_id__pk')
        print(resrv_list)
        data = duration_list.filter(~Q(pk__in=resrv_list))
        if not data.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'ok')
        return data
