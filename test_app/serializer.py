from rest_framework import serializers
from .models import PetModel
from graphene.types.scalars import Scalar


class ObjectField(Scalar):  # to serialize error message from serializer
    @staticmethod
    def serialize(dt):
        return dt


class PetSerSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        model: PetModel()

    def create(self, validated_data):
        print(validated_data)
        print('creatttttttttttttttttttttttttt')
        pet = PetModel(**validated_data)
        pet.save()
        print(pet)
        print('seeerrriririr')
        return pet

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
