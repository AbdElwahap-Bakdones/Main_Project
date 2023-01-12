
import graphene


class UserInput(graphene.InputObjectType):
    first_name = graphene.String(requierd=True)
    last_name = graphene.String(requierd=True)
    email = graphene.String(requierd=True)
    phone = graphene.Int(requierd=True)
    password = graphene.String(requierd=True)


class ManagerInput(graphene.InputObjectType):
    user = graphene.Field(UserInput)
    field = graphene.String(requierd=False)


class PlayerInput(graphene.InputObjectType):
    user = graphene.Field(UserInput)
    location_lat = graphene.String(requierd=True)
    location_long = graphene.String(requierd=True)


class SubManagerInput(graphene.InputObjectType):
    user = graphene.Field(UserInput)
    field = graphene.String(requierd=False)


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
    sub_manager_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)


class UpdateSectionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    club_id = graphene.ID()
    sub_manager_id = graphene.ID()
    is_available = graphene.Boolean()


class DeleteSectionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class AddStadiumInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    section_id = graphene.ID(required=True)
    type_id = graphene.ID(required=True)
    size = graphene.Float(required=True)
    is_available = graphene.Boolean(required=True)
    has_legua = graphene.Boolean(required=True)


class AddServiceInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class AddStadiumServiceInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    service_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)


class AddDurationInput(graphene.InputObjectType):
    time = graphene.Time(required=True)
    stad_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)
    is_deleted = graphene.Boolean(required=True)


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
