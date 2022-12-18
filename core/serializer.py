from rest_framework import serializers
from . import models
from graphene.types.scalars import Scalar


class ObjectField(Scalar):  # to serialize error message from serializer
    @staticmethod
    def serialize(dt):
        return dt


class PlayerSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'phone', 'password', 'location']

    def create(self, validated_data):
        user = models.User(**validated_data)
        user.save()
        return user
    # class UserSerializer:
