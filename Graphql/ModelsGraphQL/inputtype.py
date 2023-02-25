
import graphene
from graphene_file_upload.scalars import Upload


class UserInput(graphene.InputObjectType):
    first_name = graphene.String(requierd=True)
    last_name = graphene.String(requierd=True)
    email = graphene.String(requierd=True)
    phone = graphene.Int(requierd=True)
    password = graphene.String(requierd=True)


class ManagerInput(graphene.InputObjectType):
    user = graphene.Field(UserInput)
    is_submanager = graphene.Boolean()


class PlayerInput(graphene.InputObjectType):
    user = graphene.Field(UserInput)
    location_lat = graphene.String(requierd=True)
    location_long = graphene.String(requierd=True)
    picture = Upload(required=False)


class SubManagerInput(graphene.InputObjectType):
    user = graphene.Field(UserInput)
    club_id = graphene.ID(requierd=False)


class AddClubInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    location_lat = graphene.String(required=True)
    location_long = graphene.String(required=True)
    is_available = graphene.Boolean(default=True)


class UpdateClubInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    is_available = graphene.Boolean()


class DeleteClubInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class AddSectionInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    club_id = graphene.ID(required=True)
    sub_manager_id = graphene.ID(required=False)
    is_available = graphene.Boolean(required=False)


class UpdateSectionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    # club_id = graphene.ID()
    sub_manager_id = graphene.ID()
    is_available = graphene.Boolean()


class DeleteSectionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class AddStadiumInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    section_id = graphene.ID(required=True)
    club_id = graphene.ID(required=True)
    type_id = graphene.ID(required=True)
    size = graphene.Float(required=True)
    is_available = graphene.Boolean()
    has_legua = graphene.Boolean()
    picture = Upload()


class UpdateStadiumInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    section_id = graphene.ID()
    type_id = graphene.ID()
    size = graphene.Float()
    is_available = graphene.Boolean()
    has_legua = graphene.Boolean()


class DeleteStadiumInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class AddServiceInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class AddStadiumServiceInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    service_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)


class addtime(graphene.InputObjectType):
    start_time = graphene.Time(required=True)
    end_time = graphene.Time(required=True)
    is_available = graphene.Boolean(required=True)


class AddDurationInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    duration = graphene.List(addtime)


class updatetime(graphene.InputObjectType):
    id = graphene.ID(required=True)
    start_time = graphene.Time(required=True)
    end_time = graphene.Time(required=True)
    is_available = graphene.Boolean(required=True)


class UpdateDurationInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    duration = graphene.List(updatetime)


class deleteDuration(graphene.InputObjectType):
    id = graphene.ID(required=True)


class DeleteDurationInput(graphene.InputObjectType):
    id_list = graphene.List(graphene.ID, required=True)


class AddReservationInput(graphene.InputObjectType):
    # time = graphene.Date(required=True)
    duration_id = graphene.ID(required=True)
    kind = graphene.String(required=True)
    count = graphene.Int(required=True)
    canceled = graphene.Boolean(required=True)


class AddStadiumRateInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    rate_type_id = graphene.ID(required=True)
    value = graphene.Float(required=True)


class AddUserRateInput(graphene.InputObjectType):
    user_id = graphene.ID(required=True)
    rate_type_id = graphene.ID(required=True)
    percent = graphene.Float(required=True)


class SearchPlayerInput(graphene.InputObjectType):
    player_email = graphene.ID(required=False)
    player_Name = graphene.ID(required=False)
    # player_lastName = graphene.ID(required=False)


class AddRequestFriendInput(graphene.InputObjectType):
    player_pk = graphene.ID(required=True)


class AddTeamInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    type_id = graphene.ID(required=True)
    # picture = graphene.String(required=False)


class DeleteTeamInput(graphene.InputObjectType):
    pk = graphene.ID(required=True)


class AddMembersInput(graphene.InputObjectType):
    team_pk = graphene.ID(required=True)
    members = graphene.List(graphene.Int, required=True)


class RemoveMembersInput(graphene.InputObjectType):
    team_pk = graphene.ID(required=True)
    members = graphene.List(graphene.Int, required=True)


class LeaveTeamInput(graphene.InputObjectType):
    team_pk = graphene.ID(required=True)
