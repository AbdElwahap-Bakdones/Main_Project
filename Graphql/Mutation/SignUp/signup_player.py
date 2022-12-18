from core import models, serializer
from graphene_django import DjangoObjectType
from django.contrib.auth.hashers import make_password

import graphene


class UserModel(DjangoObjectType):
    class Meta:
        model = models.User
        fields = ['pk', 'first_name', 'last_name',
                  'location', 'email', 'phone']


class UserInput(graphene.InputObjectType):
    first_name = graphene.String(requierd=True)
    last_name = graphene.String(requierd=True)
    email = graphene.String(requierd=True)
    phone = graphene.Int(requierd=True)
    password = graphene.String(requierd=True)
    location = graphene.String(requierd=True)


def hashPassword(password: str) -> str:
    if not password == None:
        return make_password(password)
    return None


class SignUpPlayer(graphene.Mutation):
    user = graphene.Field(UserModel)
    message = graphene.String()  # serializer.ObjectField()
    status = graphene.Int()

    class Arguments:
        user_data = UserInput()

    @classmethod
    def mutate(self, root, info, **kargs):
        kargs['user_data']['username'] = kargs['user_data']['first_name'] + \
            kargs['user_data']['last_name']
        kargs['user_data']['password'] = hashPassword(
            kargs['user_data']['password'])
        print(kargs)
        seria = serializer.PlayerSerializer(
            data=kargs['user_data'])
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            # print(msg)
            status = 200
            # user = seria.save()
        else:
            msg = seria.errors
            # print(msg)
            user = None
            status = 400
        return self(user=user, message=msg, status=status)
