from graphene import ObjectType
from graphene_django.types import DjangoObjectType
from rx import Observable
import graphene
from core import models
from test_app.models import Cars
from ..Query.Club import AllClub, GetClub, MyClub
# from ..Query.Duration import searchOnReservation
from ..Query.Duration import GetAllowDuration, GetDuration
from ..Query.Section import AllSectionByClub, GetSection
from ..Query.Stadium import GetStadium, GetStadiumBySection, StadiumFilter
from ..Query.Friend import GetFriendByName, AllFriend, GetFriendById, GetFriendCanAddToTeam
from ..Auth.graphql_auth import AuthMutation
from ..Mutation.SignUp import signup
from ..Mutation.club import AddClub, UpdateClub, DeleteClub
from ..Mutation.section import AddSection, UpdateSection, DeleteSection
from ..Mutation.stadium import AddStadium, UpdateStadium
from ..Mutation.duration import AddDurationList, UpdateDurationList, DeleteDurationList
from ..Mutation.stadiumService import AddServicesForStadiums, ModificationsToStadiumServices
from ..Query import Player, Type, sub_manager, team, team_members
from ..Mutation.FriendMutat import addFriend, rejectFriend, acceptFriend
from ..Mutation.Team import createTeam, deleteTeam, addMember, leaveTeam, removeMemmber
from ..Mutation import search_on_map


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
    allSectionByClub = graphene.Field(AllSectionByClub)
    GetSection = graphene.Field(GetSection)
    getFriendByName = graphene.Field(GetFriendByName)
    getFriendById = graphene.Field(GetFriendById)
    allFriend = graphene.Field(AllFriend)
    getFriendCanAddToTeam = graphene.Field(GetFriendCanAddToTeam)
    getAllowDuration = graphene.Field(GetAllowDuration)
    serchPlayer = graphene.Field(Player.SerchPlayer)
    type_ = graphene.Field(Type.AllType)
    clubSubManager = graphene.Field(sub_manager.ClubSubManagerd)
    myClub = graphene.Field(MyClub)
    playerMe = graphene.Field(Player.me)
    findPlayerOnMap = graphene.Field(Player.GeoPlayer)
    myAllTeam = graphene.Field(team.MyAllTeam)
    myTeamByName = graphene.Field(team.SearchMyTeamByName)
    teamByName = graphene.Field(team.SearchTeamByName)
    myTeamById = graphene.Field(team.GetTeamById)
    memmberTeamById = graphene.Field(team_members.MembersTeamById)
    getStadium = graphene.Field(GetStadium)
    getStadiumBySection = graphene.Field(GetStadiumBySection)
    getDuration = graphene.Field(GetDuration)
    getPLayerById = graphene.Field(Player.GetPlayerById)
    stadiumFilter = graphene.Field(StadiumFilter)

    def resolve_stadiumFilter(root, info, **kwargs):
        return StadiumFilter()

    def resolve_getPLayerById(root, info, **kwargs):
        return Player.GetPlayerById()

    def resolve_getDuration(root, info, **kwargs):
        return GetDuration()

    def resolve_getStadiumBySection(root, info, **kwargs):
        return GetStadiumBySection()

    def resolve_getStadium(root, info, **kwargs):
        return GetStadium()

    def resolve_memmberTeamById(root, info, **kwargs):
        return team_members.MembersTeamById()

    def resolve_myTeamByName(root, info, **kwargs):
        return team.SearchMyTeamByName()

    def resolve_teamByName(root, info, **kwargs):
        return team.SearchTeamByName()

    def resolve_myTeamById(root, info, **kwargs):
        return team.GetTeamById()

    def resolve_AllClub(root, info, **kwargs):
        return AllClub()

    def resolve_GetClub(root, info, **kwargs):
        return GetClub()

    def resolve_allSectionByClub(root, info, **kwargs):
        return AllSectionByClub()

    def resolve_GetSection(root, info, **kwargs):
        return GetSection()

    def resolve_getFriendByName(root, info, **kwargsByName):
        return GetFriendByName()

    def resolve_allFriend(root, info, **kwargs):
        return AllFriend()

    def resolve_getFriendById(root, info, **kwargs):
        return GetFriendById()

    def resolve_getFriendCanAddToTeam(root, info, **kwargs):
        return GetFriendCanAddToTeam()

    def resolve_getAllowDuration(root, info, **kwargs):
        return GetAllowDuration()

    def resolve_clubSubManager(root, info, **kwargs):
        return sub_manager.ClubSubManagerd()

    def resolve_serchPlayer(root, info, **kwargs):
        return Player.SerchPlayer()

    def resolve_myClub(root, info, **kwargs):
        return MyClub()

    def resolve_type_(root, info, **kwargs):
        return Type.AllType()

    def resolve_playerMe(root, info, **kwargs):
        return Player.me()

    def resolve_findPlayerOnMap(root, info, **kwargs):
        return Player.GeoPlayer()

    def resolve_myAllTeam(root, info, **kwargs):
        return team.MyAllTeam()


class Mutation (AuthMutation, graphene.ObjectType):
    SignUpPlyer = signup.SignUpPlayer.Field(description='SignUpPlyer')
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
    addFreind = addFriend.addRequestFriend.Field()
    rejectFriend = rejectFriend.RejectFriend.Field()
    acceptFriend = acceptFriend.AcceptFriend.Field()
    createTeam = createTeam.CreateTeam.Field()
    deleteTeam = deleteTeam.DeleteTeam.Field()
    addDurationList = AddDurationList.Field()
    changeSearchMap = search_on_map.ChangeSearchOnMap.Field()
    addMember = addMember.AddMember.Field()
    leaveTeam = leaveTeam.LeaveTeam.Field()
    removeMemmbers = removeMemmber.RemoveMemmber.Field()


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
