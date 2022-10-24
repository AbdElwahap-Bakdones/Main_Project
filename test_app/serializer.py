from rest_framework import serializers
from .models import PetModel


class PetSerSerializer(serializers.Serializer):
    class Meta:
        model: PetModel()
