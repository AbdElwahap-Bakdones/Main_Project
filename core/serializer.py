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
                  'phone',  'password', 'username', 'groups']

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

    def create(self, validated_data):
        stadium = models.Stadium(**validated_data)
        stadium.save()
        return stadium


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ["id", "name"]

    def create(self, validated_data):
        service = models.Service(**validated_data)
        service.save()
        return service


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
    class Meta:
        model = models.Duration
        fields = "__all__"

    def create(self, validated_data):
        Duration = models.Duration(**validated_data)
        Duration.save()
        return Duration
