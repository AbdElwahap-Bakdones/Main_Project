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
            print(kwargs)
            data = kwargs['data']
            if models.Duration.objects.filter(id=data['duration_id']):
                # with transaction.atomic():
                duration = models.Duration.objects.select_for_update(
                    skip_locked=True
                ).filter(id=data['duration_id'])
                time.sleep(10)
                print(duration.values())
                # serializer.ReservationSerializer(data=)
            else:
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.OK(instanse=self)
        except Exception as e:
            print('Error in ReserveDuration ')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))
