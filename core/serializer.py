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
