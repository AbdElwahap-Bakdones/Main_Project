from django.db import models as MODELS, transaction
from ..ModelsGraphQL import typeobject, inputtype
from ..Auth.permission import checkPermission
import graphene
from core import models, serializer
from .. import QueryStructure
import time
from Bank import models as MODELSBANK
from Bank import views


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
            data = kwargs['data']
            if not (data['kind'] == 'team' and 'team_id' in data) and not data['kind'] == 'player':
                return QueryStructure.BadRequest(instanse=self, message='kind field is worng or team id not set !')

            if data['kind'] == 'team' and not self.is_caption(self, team_id=data['team_id'], user=user):
                return QueryStructure.BadRequest(instanse=self, message='onlay caption can reserve !')
            if data['kind'] == 'team':
                contex = {'team_id': data['team_id']}
            if data['kind'] == 'player':
                contex = {'player': models.Player.objects.filter(
                    user_id=user).get()}
            duration_obj = models.Duration.objects.filter(
                id=data['duration_id'])
            reserv_obj = models.Reservation.objects.filter(
                date=data['date'], duration_id=data['duration_id'])

            if duration_obj.exists() and not reserv_obj.exists():
                with transaction.atomic():
                    duration = models.Duration.objects.select_for_update().filter(
                        id=data['duration_id'])
                    seria = serializer.ReservationSerializer(
                        data=data, context=contex)
                    if seria.is_valid():
                        if not self.withdrawal(data['duration_id'], contex['player'].pk):
                            return QueryStructure.BadRequest(self, message="You do not have enough balance to reserve the stadium")
                        data = seria.save()
                        return QueryStructure.Created(instanse=self, data=data)
                    else:
                        return QueryStructure.NotAcceptale(instanse=self, message=seria.errors)

            else:
                return QueryStructure.NotAcceptale(instanse=self)
            return QueryStructure.OK(instanse=self)
        except Exception as e:
            print('Error in ReserveDuration ')
            print(e)
            return QueryStructure.InternalServerError(instanse=self, message=str(e))

    def is_caption(self, team_id: int, user: models.User) -> bool:
        if models.Team_members.objects.filter(team_id=team_id, team_id__deleted=False,
                                              player_id__user_id=user, is_captin=True, is_leave=False).exists():
            return True
        return False

    def withdrawal(id_duration, id_player):
        priceDuration = models.Duration.objects.get(pk=id_duration)
        player_id = ""+str(id_player)+"_" + str(1)
        club_id = "" + \
            str(priceDuration.stad_id.section_id.club_id.pk)+"_" + str(2)
        withdrawal = views.withdrawal(player_id, priceDuration.price)
        if withdrawal == -1:
            return False
        deposit = views.deposit(club_id, priceDuration.price)
        if deposit == -1:
            return False
        # balance.client_ammunt = balance.client_ammunt-priceDuration.price
        # clubBalance = MODELSBANK.Account.objects.get(
        #     client_name=""+str(priceDuration.stad_id.section_id.club_id.pk)+"_"+str(2))
        # clubBalance.client_ammunt = clubBalance.client_ammunt+priceDuration.price
        # balance.save()
        # clubBalance.save()
        return True
