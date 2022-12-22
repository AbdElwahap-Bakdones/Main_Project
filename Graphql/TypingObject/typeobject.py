from core import models
from graphene_django import DjangoObjectType
import graphene
from graphene import relay


class UserObjectType(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'firstName', 'lastname',
                  'password1', 'password2', 'phone')
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class PlayerObjectType(DjangoObjectType):
    class Meta:
        model = models.Player
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class ManagerObjectType(DjangoObjectType):
    class Meta:
        model = models.Manager
        fields = "__all__"


class SubManagerObjectType(DjangoObjectType):
    class Meta:
        model = models.SubManager
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class ClubObjectType(DjangoObjectType):
    class Meta:
        model = models.Club
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class SectionObjectType(DjangoObjectType):
    class Meta:
        model = models.Section
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class StadiumObjectType(DjangoObjectType):
    class Meta:
        model = models.Stadium
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class StadiumServiceObjectType(DjangoObjectType):
    class Meta:
        model = models.StadiumService
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class ServiceObjectType(DjangoObjectType):
    class Meta:
        model = models.Service
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class DurationObjectType(DjangoObjectType):
    class Meta:
        model = models.Duration
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class ReservationObjectType(DjangoObjectType):
    class Meta:
        model = models.Reservation
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class Player_reservationObjectType(DjangoObjectType):
    class Meta:
        model = models.Player_reservation
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class Player_reservationObjectType(DjangoObjectType):
    class Meta:
        model = models.Player_reservation
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class TeamObjectType(DjangoObjectType):
    class Meta:
        model = models.Team
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class Team_resevationObjectType(DjangoObjectType):
    class Meta:
        model = models.Team_resevation
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class Team_membersObjectType(DjangoObjectType):
    class Meta:
        model = models.Team_members
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class PostionObjectType(DjangoObjectType):
    class Meta:
        model = models.Postion
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class TypeObjectType(DjangoObjectType):
    class Meta:
        model = models.Type
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class StadiumRateObjectType(DjangoObjectType):
    class Meta:
        model = models.StadiumRate
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class UserRateObjectType(DjangoObjectType):
    class Meta:
        model = models.UserType
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class RateTypeObjectType(DjangoObjectType):
    class Meta:
        model = models.RateType
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class NotificationObjectType(DjangoObjectType):
    class Meta:
        model = models.Notification
        fields = "__all__"
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id
