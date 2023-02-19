from core import models, serializer
from graphene_django import DjangoObjectType
from graphene import relay
import graphene


class UserObjectType(DjangoObjectType):
    pk_user = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = models.User
        fields = ['pk', 'first_name', 'last_name',
                  'email', 'phone', 'username']
        interfaces = (relay.Node,)


class PlayerObjectType(DjangoObjectType):
    user_id = graphene.Field(UserObjectType)
    pk_player = graphene.Field(type=graphene.Int, source='id')
    state = graphene.Field(type=graphene.String, source='state')

    class Meta:
        model = models.Player
        fields = ['pk', 'location_lat',
                  'location_long', 'user_id', 'available_on_map']
        interfaces = (relay.Node,)


class ManagerObjectType(DjangoObjectType):
    user_id = graphene.Field(UserObjectType)
    pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = models.Manager
        fields = ['id,pk,user_id']


class SubManagerObjectType(DjangoObjectType):
    user_id = graphene.Field(UserObjectType)
    pk = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = models.SubManager
        fields = ['id', 'pk', 'user_id']
        interfaces = (relay.Node,)


class TypeObjectType(DjangoObjectType):
    pk_type = graphene.Field(type=graphene.Int, source='id')

    class Meta:

        model = models.Type
        fields = ['pk', 'name']
        interfaces = (relay.Node,)


class ClubObjectType(DjangoObjectType):
    manager = graphene.Field(ManagerObjectType, source='manager_id')
    pk_club = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = models.Club
        fields = ['id', 'pk', 'name', 'location_lat', 'location_long',
                  'number_stad', 'is_available', 'manager_id']
        interfaces = (relay.Node,)


class SectionObjectType(DjangoObjectType):
    pk_sectaion = graphene.Field(type=graphene.Int, source='id')
    sub_manager = graphene.Field(
        SubManagerObjectType, source='sub_manager_id')

    class Meta:
        model = models.Section
        fields = ['name', 'is_available',
                  'club_id']
        interfaces = (relay.Node,)


class StadiumObjectType(DjangoObjectType):
    pk_stadium = graphene.Field(type=graphene.Int, source='id')
    section = graphene.Field(type=SectionObjectType, source='section_id')
    type_ = graphene.Field(type=TypeObjectType, source='type_id')

    class Meta:
        model = models.Stadium
        fields = ['id', 'pk', 'name', 'is_available',
                  'has_legua', 'size', 'picture']
        interfaces = (relay.Node,)


class ServiceObjectType(DjangoObjectType):
    pk_service = graphene.Field(type=graphene.Int, source='id')

    class Meta:
        model = models.Service
        fields = ['id', 'pk', 'name']
        interfaces = (relay.Node,)


class StadiumServiceObjectType(DjangoObjectType):
    pk_stadium_service = graphene.Field(type=graphene.Int, source='id')
    service = graphene.Field(type=ServiceObjectType, source='service_id')
    stadium = graphene.Field(type=StadiumObjectType, source='stad_id')

    class Meta:
        model = models.StadiumService
        fields = ['id', 'pk', 'stad_id', 'service_id', 'is_available']
        interfaces = (relay.Node,)


class DurationObjectType(DjangoObjectType):
    pk_duration = graphene.Field(type=graphene.Int, source='id')
    stadium = graphene.Field(type=StadiumObjectType, source='stad_id')

    class Meta:
        model = models.Duration
        fields = ['id', 'pk', 'start_time', 'end_time', 'is_available']
        interfaces = (relay.Node,)


class ReservationObjectType(DjangoObjectType):
    pk_reservation = graphene.Field(type=graphene.Int, source='id')
    duration = graphene.Field(type=DurationObjectType, source='duration_id')

    class Meta:
        model = models.Reservation
        fields = ['id', 'pk', 'duration_id',
                  'kind', 'count', 'time', 'canceled']
        interfaces = (relay.Node,)


class Player_reservationObjectType(DjangoObjectType):
    pk_player_reservation = graphene.Field(type=graphene.Int, source='id')
    reservation = graphene.Field(
        type=ReservationObjectType, source='reservation_id')
    player = graphene.Field(
        type=PlayerObjectType, source='player_id')

    class Meta:
        model = models.Player_reservation
        fields = ['id', 'pk', 'player_id', 'reservation_id']
        interfaces = (relay.Node,)


class TeamObjectType(DjangoObjectType):
    pk_team = graphene.Field(type=graphene.Int, source='id')
    type_ = graphene.Field(type=TypeObjectType, source='type_id')

    class Meta:
        model = models.Team
        fields = ['pk', 'name', 'type_id',
                  'search_game', 'member_count', 'temp']
        interfaces = (relay.Node,)


class Team_resevationObjectType(DjangoObjectType):
    pk_team_resevation = graphene.Field(type=graphene.Int, source='id')
    reservation = graphene.Field(
        type=ReservationObjectType, source='reservation_id')
    team = graphene.Field(type=TeamObjectType, source='team_id')

    class Meta:
        model = models.Team_resevation
        fields = ['id', 'pk', 'team_id', 'reservation_id']
        interfaces = (relay.Node,)


class PositionObjectType(DjangoObjectType):
    class Meta:
        model = models.Position
        fields = "__all__"
        interfaces = (relay.Node,)


class Team_membersObjectType(DjangoObjectType):
    member = graphene.Field(type=PlayerObjectType, source='player_id')
    position = graphene.Field(type=PositionObjectType, source='position_id')

    class Meta:
        model = models.Team_members
        fields = ['member', 'position', 'is_captin']
        interfaces = (relay.Node,)


class StadiumRateObjectType(DjangoObjectType):
    class Meta:
        model = models.StadiumRate
        fields = "__all__"
        interfaces = (relay.Node,)


class UserRateObjectType(DjangoObjectType):
    class Meta:
        model = models.UserRate
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


class FriendObjectType(DjangoObjectType):
    pk_friend = graphene.Field(type=graphene.Int, source='id')
    friends = graphene.Field(type=PlayerObjectType, source='player2')
    me = graphene.Field(type=graphene.ID, source='player1')

    class Meta:
        model = models.Friend
        fields = ['pk', 'friends', 'me']
        interfaces = (relay.Node,)
