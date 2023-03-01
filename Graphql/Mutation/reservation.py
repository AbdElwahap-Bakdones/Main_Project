from django.db import models as MODELS, transaction
from ..ModelsGraphQL import typeobject, inputtype
from ..Auth.permission import checkPermission
import graphene
from core import models, serializer
from .. import QueryStructure
import time


class ReserveDuration  (graphene.Mutation, QueryStructure.Attributes):

    data = graphene.Field(typeobject.ReservationObjectType)

    class Arguments:
        data = inputtype.AddReservationInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.add_reservation", user):
                return QueryStructure.NoPermission(self)
            # print(kwargs)
            data = kwargs['data']
            duration_obj = models.Duration.objects.filter(
                id=data['duration_id'])
            reserv_obj = models.Reservation.objects.filter(
                date=data['date'], duration_id=data['duration_id'])
            if duration_obj.exists() and not reserv_obj.exists():
                with transaction.atomic():
                    duration = models.Duration.objects.select_for_update().filter(
                        id=data['duration_id'])
                    # data['duration_id'] = duration.get()
                    print(data)
                    seria = serializer.ReservationSerializer(data=data)
                    if seria.is_valid():
                        reserv = models.Reservation()
                        data = seria.save()
                        return QueryStructure.Created(instanse=self, data=data)
                    else:
                        return QueryStructure.BadRequest(instanse=self, message=seria.errors)

            else:
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.OK(instanse=self)
        except Exception as e:
            print('Error in ReserveDuration ')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))
