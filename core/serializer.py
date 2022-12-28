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
        fields = ["pk", "manager_id", "number_stad", "name",
                  "location", "is_available", "is_deleted"]

    def create(self, validated_data):
        club = models.Club(**validated_data)
        club.save()
        return club
    # class UserSerializer:

    def update(self, instance, validated_data):
        print(validated_data.get('name', instance.name))
        instance.name = validated_data.get('name', instance.name)
        instance.is_available = validated_data.get(
            'is_available', instance.is_available)
        instance.number_stad = validated_data.get(
            'number_stad', instance.number_stad)
        instance.is_deleted = validated_data.get(
            'is_deleted', instance.is_deleted)
        instance.location = validated_data.get(
            'location', instance.location)

        instance.save()
        print(instance.name)
        return instance


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
    stad_id = StadiumSerializer

    class Meta:
        model = models.Duration
        fields = ["id", "stad_id", "is_available", "is_deleted", "time"]

    def create(self, validated_data):
        Duration = models.Duration(**validated_data)
        Duration.save()
        return Duration


class ReservationSerializer(serializers.ModelSerializer):
    duration_id = DurationSerializer

    class Meta:
        model = models.Reservation
        fields = ["id", "duration_id", "kind", "count", "canceled"]

    def create(self, validated_data):
        reservation = models.Reservation(**validated_data)
        reservation.save()
        return reservation


class RateTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RateType
        fields = ["id", "name", "value"]

    def create(self, validated_data):
        rateType = models.RateType(**validated_data)
        rateType.save()
        return rateType


class UserRateSerializer(serializers.ModelSerializer):
    user_id = UserSerializer
    rateType_id = RateTypeSerializer

    class Meta:
        model = models.UserRate
        fields = ["id", "user_id", "rateType_id", "percent"]

    def create(self, validated_data):
        userRate = models.UserRate(**validated_data)
        userRate.save()
        return userRate


class StadiumRateRateSerializer(serializers.ModelSerializer):
    stad_id = StadiumSerializer
    rate_type_id = RateTypeSerializer

    class Meta:
        model = models.StadiumRate
        fields = ["id", "stad_id", "rate_type_id", "value"]

    def create(self, validated_data):
        stadiumRate = models.StadiumRate(**validated_data)
        stadiumRate.save()
        return stadiumRate
