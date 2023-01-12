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
from ..Query.Duration import searchOnReservation
from ..Query.Section import AllSection, GetSection
from ..Query.Friend import GetFriend, AllFriend
from ..Query.Userteam import AllTeamMembers
from ..Query.team import GetTeam
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
    myteam = graphene.Field(AllTeamMembers)
    getTeam = graphene.Field(GetTeam)
    searchonReservation = graphene.Field(searchOnReservation)
    serchPlayer = graphene.Field(Player.SerchPlayer)

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

    def resolve_myteam(root, info, **kwargs):
        return AllTeamMembers()

    def resolve_getTeam(root, info, **kwargs):
        return GetTeam()

    def resolve_searchonReservation(root, info, **kwargs):
        return searchOnReservation()

    def resolve_serchPlayer(root, info, **kwargs):
        return Player.SerchPlayer()


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
