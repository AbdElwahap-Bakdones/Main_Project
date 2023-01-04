from rest_framework import serializers
from .models import PetModel, Compani


class PetSerSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        model: PetModel()

    def create(self, validated_data):
        pet = PetModel(**validated_data)
        pet.save()
        return pet

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class CompSeria(serializers.Serializer):
    class Meta:
        model: Compani()
        fields: ['id']
