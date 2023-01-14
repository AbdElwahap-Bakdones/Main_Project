from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Rule(models.Model):
    name = models.CharField(max_length=255)
    auth = models.TextField(blank=True)


class User(AbstractUser):
    phone = models.IntegerField(default=930075476, blank=False)
    first_name = models.CharField(('first name'), max_length=150, blank=False)
    last_name = models.CharField(('last name'), max_length=150, blank=False)
    email = models.EmailField(('email address'), blank=False, unique=True)
    rule_id = models.ForeignKey(Rule, on_delete=models.CASCADE, default=1)
    # picture = models.ImageField()
    # USERNAME_FIELD = "username"   # e.g: "username", "email"
    # EMAIL_FIELD = "email"         # e.g: "email", "primary_email"

    def __str__(self):
        return str(self.username)


class permission(models.Model):
    name = models.CharField(max_length=255)
    rule_id = models.ForeignKey(Rule, on_delete=models.CASCADE)


class RateType(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()


class UserRate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rate_type_id = models.ForeignKey(RateType, on_delete=models.CASCADE)
    percent = models.FloatField()


class Manager(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username


class Player(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    location_lat = models.CharField(max_length=255)
    location_long = models.CharField(max_length=255)

    def __str__(self):
        return self.user_id.username


class Type(models.Model):
    name = models.CharField(max_length=255)


class Club(models.Model):
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number_stad = models.IntegerField(default=0)
    location_lat = models.CharField(max_length=255)
    location_long = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


class SubManager(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.username


class Section(models.Model):
    sub_manager_id = models.ForeignKey(SubManager, on_delete=models.CASCADE)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


class Stadium(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    has_legua = models.BooleanField(default=False)
    size = models.FloatField()


class StadiumRate(models.Model):
    stad_id = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    rate_type_id = models.ForeignKey(RateType, on_delete=models.CASCADE)
    percent = models.FloatField()


class Duration(models.Model):
    stad_id = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


class Service(models.Model):
    name = models.CharField(max_length=255)


class StadiumService(models.Model):
    stad_id = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)


class Reservation(models.Model):
    duration_id = models.ForeignKey(Duration, on_delete=models.CASCADE)
    kind = models.CharField(max_length=255)
    count = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    canceled = models.BooleanField(default=False)


class Player_reservation(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField()
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=True)
    search_game = models.BooleanField(default=True)
    temp = models.BooleanField(default=True)


class Team_resevation(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)


class Position(models.Model):

    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)


class Team_members(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_captin = models.BooleanField(default=True)
    is_leave = models.BooleanField(default=False)


class Notification(models.Model):
    reciver_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reciver_id')
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender_id')
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender_kind = models.CharField(max_length=255)
    content = models.CharField(max_length=255)


class Friend(models.Model):
    player1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='player11', null=True)
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='player22', null=True)
    sender = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='sender', null=True)
    art = [('accepted', 'accepted'), ('rejected',
                                      'rejected'), ('pending', 'pending')]
    state = models.CharField(choices=art, max_length=30, default='pending')
