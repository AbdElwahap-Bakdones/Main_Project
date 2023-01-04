from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django import DjangoListField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphql.execution.base import ResolveInfo
from graphql.language.ast import Field, SelectionSet
from graphene_django.views import GraphQLView
from rx import Observable
from rest_framework import status as status_code
import graphene

from core import models
from Graphql.QueryStructure import QueryFields
from test_app.models import Cars, Compani
from ..Query.Club import AllClub
from graphql_auth.schema import UserQuery, MeQuery
from ..Auth.graphql_auth import AuthMutation
from ..Mutation.SignUp import signup
from ..Mutation.club import AddClub, UpdateClub
from ..Mutation.section import AddSection, UpdatSection
from ..Mutation.stadium import AddStadium, UpdateStadium
from ..Mutation.service import AddService, UpdateService
from ..Mutation.stadiumService import AddServicesForStadiums, ModificationsToStadiumServices


class User_model(DjangoObjectType):

    class Meta:
        model = models.User
        fields = ['username']


class Query(ObjectType):
    # token_auth = mutations.ObtainJSONWebToken.Field()

    hello = graphene.Field(User_model)

    def resolve_hello(root, info, **kwargs):
        print('ppppppppppppppp')
        print(kwargs)
        return models.User.objects.filter(pk=2)

    AllClub1 = graphene.Field(AllClub)

    def resolve_AllClub1(root, info, **kwargs):
        return AllClub()


class Mutation (AuthMutation, graphene.ObjectType):
    SignUpPlyer = signup.SignUpPlayer.Field()
    SignUpManager = signup.SignUpManager.Field()
    SignUpSubManager = signup.SignUpSubManager.Field()
    addclub = AddClub.Field()
    updateclub = UpdateClub.Field()
    addsection = AddSection.Field()
    updatesection = UpdatSection.Field()
    addstadium = AddStadium.Field()
    updatestadium = UpdateStadium.Field()
    addservice = AddService.Field()
    updateservice = UpdateService.Field()
    addservicesforstadiums = AddServicesForStadiums.Field()
    modificationstostadiumservices = ModificationsToStadiumServices.Field()


class Subscription(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        print('ssssssssssssssssssssssss')

        return Observable.interval(3000).map(lambda i: i)

    def resolve_cars_created(root, info):
        print('create cars')

        return root.filter(
            lambda event:
                event.operation == CREATED and
                isinstance(event.instance, Cars)
        ).map(lambda event: event.instance)


schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)
