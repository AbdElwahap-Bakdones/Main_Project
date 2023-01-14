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
from ..Query.Club import AllClub, GetClub
from ..Query.Duration import GetAllowDuration
from ..Query.Section import AllSection, GetSection
from ..Query.Stadium import AllStadiumByType, GetStadium, GetStadiumByType
from ..Query.Friend import GetFriend, AllFriend
from ..Query.team import GetTeam, AllMyTeam, GetMyTeam
from graphql_auth.schema import UserQuery, MeQuery
from ..Auth.graphql_auth import AuthMutation
from ..Mutation.SignUp import signup
from ..Mutation.club import AddClub, UpdateClub, DeleteClub
from ..Mutation.section import AddSection, UpdateSection, DeleteSection
from ..Mutation.stadium import AddStadium, UpdateStadium
#from ..Mutation.service import AddService, UpdateService
from ..Mutation.stadiumService import AddServicesForStadiums, ModificationsToStadiumServices
from ..Query import Player


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

    AllClub = graphene.Field(AllClub)
    GetClub = graphene.Field(GetClub)
    AllSection = graphene.Field(AllSection)
    GetSection = graphene.Field(GetSection)
    getFriend = graphene.Field(GetFriend)
    allFriend = graphene.Field(AllFriend)
    getAllowDuration = graphene.Field(GetAllowDuration)
    serchPlayer = graphene.Field(Player.SerchPlayer)
    getTeam = graphene.Field(GetTeam)
    allMyTeam = graphene.Field(AllMyTeam)
    getMyTeam = graphene.Field(GetMyTeam)
    getStadium = graphene.Field(GetStadium)
    allStadiumByType = graphene.Field(AllStadiumByType)
    getStadiumByType = graphene.Field(GetStadiumByType)

    def resolve_AllClub(root, info, **kwargs):
        return AllClub()

    def resolve_GetClub(root, info, **kwargs):
        return GetClub()

    def resolve_AllSection(root, info, **kwargs):
        return AllSection()

    def resolve_GetSection(root, info, **kwargs):
        return GetSection()

    def resolve_getFriend(root, info, **kwargs):
        return GetFriend()

    def resolve_allFriend(root, info, **kwargs):
        return AllFriend()

    def resolve_getTeam(root, info, **kwargs):
        return GetTeam()

    def resolve_getAllowDuration(root, info, **kwargs):
        return GetAllowDuration()

    def resolve_serchPlayer(root, info, **kwargs):
        return Player.SerchPlayer()

    def resolve_allMyTeam(root, info, **kwargs):
        return AllMyTeam()

    def resolve_getMyTeam(root, info, **kwargs):
        return GetMyTeam()

    def resolve_getStadium(root, info, **kwargs):
        return GetStadium()

    def resolve_allStadiumByType(root, info, **kwargs):
        return AllStadiumByType()

    def resolve_getStadiumByType(root, info, **kwargs):
        return GetStadiumByType()


class Mutation (AuthMutation, graphene.ObjectType):
    SignUpPlyer = signup.SignUpPlayer.Field()
    SignUpManager = signup.SignUpManager.Field()
    SignUpSubManager = signup.SignUpSubManager.Field()
    addclub = AddClub.Field()
    updateclub = UpdateClub.Field()
    deleteclub = DeleteClub.Field()
    addsection = AddSection.Field()
    updatesection = UpdateSection.Field()
    deletesection = DeleteSection.Field()
    addstadium = AddStadium.Field()
    updatestadium = UpdateStadium.Field()
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
