from rest_framework import serializers
from . import models
from django.contrib.auth.hashers import make_password

def hashPassword(password: str) -> str:
    if not password == None:
        return make_password(password)
    return None


class RuleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    # class Meta:
    #     model = models.Rule
    #     fields = '__all__'
class PlayerSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # rule_id = RuleSerializer
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email',
                  'phone',  'password','location']

    def create(self, validated_data):
        print(validated_data)
        validated_data['username']=validated_data['first_name']+'$'+validated_data['last_name']
        validated_data['password']=hashPassword(validated_data['password'])
        user = models.User(**validated_data)
        user.save()
        return user
    # class UserSerializer:
