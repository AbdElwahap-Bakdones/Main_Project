from core.models import Duration, Reservation, Club, Section, Stadium, Player_reservation, Team_resevation, Team_members, User, Team
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
from django.db.models import Q, Field, OuterRef, Subquery, F
from datetime import datetime
from itertools import chain
import graphene


class ReservationManager(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.ReservationConnection, date=graphene.Date(required=True), stadium=graphene.ID(), section=graphene.ID(), club=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        typeuser = "manager"
        if not QueryFields.is_valide(info, user, 'core.change_stadium'):
            return QueryFields.rise_error(user)
        if not QueryFields.is_valide(info, user, 'core.change_club'):
            typeuser = "submanager"
        if typeuser == "submanager":
            club = getclub(kwargs['club'])
        else:
            club = getclub(kwargs['club'], user=user)
        print("1")
        if club.__len__() == 0:
            return QueryFields.NotFound(info=info)
        if 'section' in kwargs:
            if typeuser == "submanager":
                QueryFields.BadRequest(info)
            section = getsectionlist(club, section=kwargs['section'])
        else:
            section = getsectionlist(club)
        print("2")
        if section.__len__() == 0:
            return QueryFields.NotFound(info=info)
        if 'stadium' in kwargs:
            if typeuser == "submanager":
                stadium = getstadiumlist(
                    section, stadium=kwargs['stadium'], user=user)

            print("kokoo")
            stadium = getstadiumlist(section, stadium=kwargs['stadium'])
        else:
            stadium = getstadiumlist(section)
        print("3")
        if stadium.__len__() == 0:
            return QueryFields.NotFound(info=info)
        duration = getdurationlist(stadium)
        print("4")
        if duration.__len__() == 0:
            return QueryFields.NotFound(info=info)
        data = Reservation.objects.filter(
            duration_id__in=duration, date__date=kwargs['date'], canceled=False)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


class ReservationPlayer(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.Player_reservationConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_player_reservation'):
            return QueryFields.rise_error(user)
        club = getclublist()
        if club.__len__() == 0:
            return QueryFields.NotFound(info=info)
        section = getsectionlist(club)
        if section.__len__() == 0:
            return QueryFields.NotFound(info=info)
        stadium = getstadiumlist(section)
        if stadium.__len__() == 0:
            return QueryFields.NotFound(info=info)
        duration = getdurationlist(stadium)
        if duration.__len__() == 0:
            return QueryFields.NotFound(info=info)
        reservation = Reservation.objects.filter(
            duration_id__in=duration, canceled=False).values_list('id', flat=True)
        if reservation.__len__() == 0:
            return QueryFields.NotFound(info=info)
        data = Player_reservation.objects.filter(
            player_id__user_id=user, reservation_id__in=reservation)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)


def getclub(club_id, **kwargs):
    club = Club.objects.filter(
        id=club_id, is_available=True, is_deleted=False)
    if 'user' in kwargs:
        club = club.filter(manager_id__user_id=kwargs['user'])
    return club.values_list('id', flat=True)


def getclublist(**kwargs):
    club = Club.objects.filter(is_available=True, is_deleted=False)
    if 'user' in kwargs:
        club = club.filter(manager_id__user_id=kwargs['user'])
    if 'club_id' in kwargs:
        club = club.filter(id=kwargs['club_id'])
    return club.values_list('id', flat=True)


def getsectionlist(club, **kwargs):
    print(club)
    section = Section.objects.filter(
        club_id__in=club, is_available=True, is_deleted=False)
    if 'section' in kwargs:
        section = section.filter(id=kwargs['section'])
    if 'user' in kwargs:
        section = section.filter(club_id__manager_id__user_id=kwargs['user'])
    return section.values_list('id', flat=True)


def getstadiumlist(section, **kwargs):
    stadium = Stadium.objects.filter(
        section_id__in=section, is_available=True, is_deleted=False)
    if 'stadium' in kwargs:
        stadium = stadium.filter(id=kwargs['stadium'])
    if 'user' in kwargs:
        stadium = stadium.filter(
            section_id__sub_manager_id__user_id=kwargs['user'])
    return stadium.values_list('id', flat=True)


def getdurationlist(stadium):
    print(stadium)
    return Duration.objects.filter(
        stad_id__in=stadium, is_available=True, is_deleted=False).values_list('id', flat=True)


def getteamlist(user):
    return Team_members.objects.filter(player_id__user_id=user)


class MyAllReservation(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.ReservationConnection,
                                 player_reserve=graphene.Boolean(), team_reserve=graphene.Boolean())

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_player_reservation'):
                return QueryFields.rise_error(user)
            player_reserve = team_reserve = None
            player_reserve = MyAllReservation.get_player_reserve(
                user=user, kwargs=kwargs)
            team_reserve = MyAllReservation.get_team_reserve(
                user=user, kwargs=kwargs)

            all_reserve = player_reserve | team_reserve
            data = all_reserve.order_by('-date')
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('Error in MyAllReservation.resolve_data')
            print(e)
            return QueryFields.ServerError(info=info, msg=str(e))

    def get_player_reserve(user: User, kwargs: bool) -> Reservation.objects:
        if 'player_reserve' in kwargs and kwargs['player_reserve']:
            player_OuterRef = Player_reservation.objects.filter(
                reservation_id=OuterRef('pk'))
            reserver_list = Player_reservation.objects.filter(
                player_id__user_id=user).values_list('reservation_id', flat=True)
            reserve_obj = Reservation.objects.filter(pk__in=reserver_list, canceled=False).annotate(
                owner=Subquery(player_OuterRef.values('player_id__user_id__username'), output_field=Field()))

            return reserve_obj
        return Reservation.objects.filter(pk=-1)

    def get_team_reserve(user: User, kwargs: bool) -> Reservation.objects:
        if 'team_reserve' in kwargs and kwargs['team_reserve']:
            team_OuterRef = Team_resevation.objects.filter(
                reservation_id=OuterRef('pk'))

            team_list = Team_members.objects.filter(
                player_id__user_id=user.pk, is_leave=False).values_list('team_id', flat=True)
            reserver_list = Team_resevation.objects.filter(
                team_id__in=team_list).values_list('reservation_id', flat=True)
            reserve_obj = Reservation.objects.filter(pk__in=reserver_list, canceled=False).annotate(
                owner=Subquery(team_OuterRef.values('team_id__name'), output_field=Field()))
            return reserve_obj
        return Reservation.objects.filter(pk=-1)
