from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password


def hashPassword(password: str) -> str:
    if not password == None:
        return make_password(password)
    return None


class RuleSerializer(serializers.Serializer):
    class Meta:
        model = models.Rule
        fields = '__all__'


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

    class Meta:
        model = models.Player
        fields = ['location_lat', 'location_long', 'user_id']


class ManagerSerializer(serializers.ModelSerializer):
    user_id = UserSerializer

    class Meta:
        model = models.Manager
        fields = ['user_id']


class SubManagerSerializer(serializers.ModelSerializer):
    user_id = UserSerializer

    class Meta:
        model = models.SubManager
        fields = ['user_id']


class ClubSerializer(serializers.ModelSerializer):
    manager_id = ManagerSerializer

    class Meta:
        model = models.Club
        fields = ["id", "manager_id", "number_stad", "name",
                  "location", "is_available"]

    def create(self, validated_data):
        club = models.Club(**validated_data)
        club.save()
        return club
    # class UserSerializer:


class SectionSerializer(serializers.ModelSerializer):
    sub_manager_id = SubManagerSerializer
    club_id = ClubSerializer

    class Meta:
        model = models.Section
        fields = ["id", "name", "sub_manager_id", "club_id", "is_available"]

    def create(self, validated_data):
        section = models.Section(**validated_data)
        section.save()
        return section


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stadium
        fields = "__all__"

    def create(self, validated_data):
        Stadium = models.Stadium(**validated_data)
        Stadium.save()
        return Stadium


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = "__all__"

    def create(self, validated_data):
        Service = models.Service(**validated_data)
        Service.save()
        return Service


class StadiumServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StadiumService
        fields = "__all__"

    def create(self, validated_data):
        StadiumService = models.StadiumService(**validated_data)
        StadiumService.save()
        return StadiumService


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Duration
        fields = "__all__"

    def create(self, validated_data):
        Duration = models.Duration(**validated_data)
        Duration.save()
        return Duration
