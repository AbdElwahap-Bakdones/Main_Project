from TypingObject import typeobject
from graphene import relay


class UserConnection(relay.Connection):
    class Meta:
        node = typeobject.UserObjectType


class PlayerConnection(relay.Connection):
    class Meta:
        node = typeobject.PlayerObjectType


class SubManagerConnection(relay.Connection):
    class Meta:
        node = typeobject.SubManagerObjectType


class ClubConnection(relay.Connection):
    class Meta:
        node = typeobject.ClubObjectType


class SectionConnection(relay.Connection):
    class Meta:
        node = typeobject.SectionObjectType


class StadiumConnection(relay.Connection):
    class Meta:
        node = typeobject.StadiumObjectType


class StadiumServiceConnection(relay.Connection):
    class Meta:
        node = typeobject.StadiumServiceObjectType


class ServiceConnection(relay.Connection):
    class Meta:
        node = typeobject.ServiceObjectType


class DurationConnection(relay.Connection):
    class Meta:
        node = typeobject.DurationObjectType


class ReservationConnection(relay.Connection):
    class Meta:
        node = typeobject.ReservationObjectType


class Player_reservationConnection(relay.Connection):
    class Meta:
        node = typeobject.Player_reservationObjectType


class TeamConnection(relay.Connection):
    class Meta:
        node = typeobject.TeamObjectType


class Team_resevationConnection(relay.Connection):
    class Meta:
        node = typeobject.Team_resevationObjectType


class Team_membersConnection(relay.Connection):
    class Meta:
        node = typeobject.Team_membersObjectType


class PostionConnection(relay.Connection):
    class Meta:
        node = typeobject.PostionObjectType


class TypeConnection(relay.Connection):
    class Meta:
        node = typeobject.TypeObjectType


class StadiumRateConnection(relay.Connection):
    class Meta:
        node = typeobject.StadiumRateObjectType


class UserRateConnection(relay.Connection):
    class Meta:
        node = typeobject.UserRateObjectType


class RateTypeConnection(relay.Connection):
    class Meta:
        node = typeobject.RateTypeObjectType


class NotificationConnection(relay.Connection):
    class Meta:
        node = typeobject.NotificationObjectType
