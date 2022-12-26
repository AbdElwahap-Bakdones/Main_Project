from core import models
from graphene_django import DjangoObjectType
import graphene
from graphene import relay


class UserObjectType(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ('pk', 'username', 'firstName', 'lastname', 'phone')
        interfaces = (relay.Node,)


class PlayerObjectType(DjangoObjectType):
    class Meta:
        model = models.Player
        fields = "__all__"
        interfaces = (relay.Node,)


class ManagerObjectType(DjangoObjectType):
    class Meta:
        model = models.Manager
        fields = "__all__"


class SubManagerObjectType(DjangoObjectType):
    class Meta:
        model = models.SubManager
        fields = "__all__"
        interfaces = (relay.Node,)


class ClubObjectType(DjangoObjectType):
    class Meta:
        model = models.Club
        fields = "__all__"
        interfaces = (relay.Node,)


class SectionObjectType(DjangoObjectType):
    class Meta:
        model = models.Section
        fields = "__all__"
        interfaces = (relay.Node,)


class StadiumObjectType(DjangoObjectType):
    class Meta:
        model = models.Stadium
        fields = "__all__"
        interfaces = (relay.Node,)


class StadiumServiceObjectType(DjangoObjectType):
    class Meta:
        model = models.StadiumService
        fields = "__all__"
        interfaces = (relay.Node,)


class ServiceObjectType(DjangoObjectType):
    class Meta:
        model = models.Service
        fields = "__all__"
        interfaces = (relay.Node,)


class DurationObjectType(DjangoObjectType):
    class Meta:
        model = models.Duration
        fields = "__all__"
        interfaces = (relay.Node,)


class ReservationObjectType(DjangoObjectType):
    class Meta:
        model = models.Reservation
        fields = "__all__"
        interfaces = (relay.Node,)


class Player_reservationObjectType(DjangoObjectType):
    class Meta:
        model = models.Player_reservation
        fields = "__all__"
        interfaces = (relay.Node,)


class Player_reservationObjectType(DjangoObjectType):
    class Meta:
        model = models.Player_reservation
        fields = "__all__"
        interfaces = (relay.Node,)


class TeamObjectType(DjangoObjectType):
    class Meta:
        model = models.Team
        fields = "__all__"
        interfaces = (relay.Node,)


class Team_resevationObjectType(DjangoObjectType):
    class Meta:
        model = models.Team_resevation
        fields = "__all__"
        interfaces = (relay.Node,)


class Team_membersObjectType(DjangoObjectType):
    class Meta:
        model = models.Team_members
        fields = "__all__"
        interfaces = (relay.Node,)


class PostionObjectType(DjangoObjectType):
    class Meta:
        model = models.Postion
        fields = "__all__"
        interfaces = (relay.Node,)


class TypeObjectType(DjangoObjectType):
    class Meta:
        model = models.Type
        fields = "__all__"
        interfaces = (relay.Node,)


class StadiumRateObjectType(DjangoObjectType):
    class Meta:
        model = models.StadiumRate
        fields = "__all__"
        interfaces = (relay.Node,)


class UserRateObjectType(DjangoObjectType):
    class Meta:
        model = models.UserType
        fields = "__all__"
        interfaces = (relay.Node,)


class RateTypeObjectType(DjangoObjectType):
    class Meta:
        model = models.RateType
        fields = "__all__"
        interfaces = (relay.Node,)


class NotificationObjectType(DjangoObjectType):
    class Meta:
        model = models.Notification
        fields = "__all__"
        interfaces = (relay.Node,)
