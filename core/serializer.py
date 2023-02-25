from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password
from core import Geo


def hashPassword(password: str) -> str:
    if not password == None:
        return make_password(password)
    return None


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email',
                  'phone',  'password', 'username']

    def create(self, validated_data):
        validated_data['password'] = hashPassword(validated_data['password'])
        user = models.User(**validated_data)
        user.save()
        return user


class PlayerSerializer(serializers.ModelSerializer):
    user_id = UserSerializer
    # state = serializers.SerializerMethodField(method_name='get_state')

    class Meta:
        model = models.Player
        fields = ['location_lat', 'location_long', 'user_id']

    def create(self, validated_data):
        validated_data = Geo.set_point_field(validated_data)
        return models.Player.objects.create(**validated_data)

    # def get_state(self, validated_data):
    #     return 'state'


class ManagerSerializer(serializers.ModelSerializer):
    user_id = UserSerializer

    class Meta:
        model = models.Manager
        fields = ['user_id']


class SubManagerSerializer(serializers.ModelSerializer):
    user_id = UserSerializer

    class Meta:
        model = models.SubManager
        fields = ['user_id', 'club_id']


class ClubSerializer(serializers.ModelSerializer):
    manager_id = ManagerSerializer

    class Meta:
        model = models.Club
        fields = ["pk", "manager_id", "number_stad", "name",
                  "location_lat", "location_long", "is_available", "is_deleted"]

    # def create(self, validated_data):
    #     club = models.Club(**validated_data)
    #     club.save()
    #     return club

    # def update(self, instance, validated_data):
    #     print(validated_data.get('name', instance.name))
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.is_available = validated_data.get(
    #         'is_available', instance.is_available)
    #     instance.is_deleted = validated_data.get(
    #         'is_deleted', instance.is_deleted)
    #     instance.save()
    #     print(instance.name)
    #     return instance


class SectionSerializer(serializers.ModelSerializer):
    sub_manager_id = SubManagerSerializer
    club_id = ClubSerializer

    class Meta:
        model = models.Section
        fields = ["name", "sub_manager_id",
                  "club_id", "is_available", "is_deleted"]


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Type
        fields = "__all__"

    def create(self, validated_data):
        types = models.Type(**validated_data)
        types.save()
        return types


class StadiumSerializer(serializers.ModelSerializer):
    section_id = SectionSerializer
    type_id = TypeSerializer

    class Meta:
        model = models.Stadium
        fields = ["id", "name", "section_id",
                  "type_id", "size", "is_available"]

    # def create(self, validated_data):
    #     stadium = models.Stadium(**validated_data)
    #     stadium.save()
    #     return stadium


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ["id", "name"]


class StadiumServiceSerializer(serializers.ModelSerializer):
    stad_id = StadiumSerializer
    service_id = ServiceSerializer

    class Meta:
        model = models.StadiumService
        fields = ["id", "stad_id", "service_id", "is_available"]

    def create(self, validated_data):
        stadiumService = models.StadiumService(**validated_data)
        stadiumService.save()
        return stadiumService


class DurationSerializer(serializers.ModelSerializer):
    stad_id = StadiumSerializer

    class Meta:
        model = models.Duration
        fields = ["id", "stad_id", "start_time", "price",
                  "end_time", "is_available", "is_deleted"]

    def create(self, validated_data):
        Duration = models.Duration(**validated_data)
        Duration.save()
        return Duration


class FrienfSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Friend
        fields = '__all__'


class MembersTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team_members
        fields = '__all__'

    def create(self, validated_data):
        is_member_found = models.Team_members.objects.filter(
            player_id=validated_data['player_id'], is_captin=False, team_id=validated_data['team_id'])
        if not is_member_found.exists():
            return super().create(validated_data)
        return is_member_found.update(is_leave=False)


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Team
        fields = ['name', 'picture', 'type_id', 'search_game']
