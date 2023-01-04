
import graphene


class AddClubInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    location = graphene.String(required=True)
    is_available = graphene.Boolean(default=True)


class InputUpdateClub(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String()
    location = graphene.String()
    is_available = graphene.Boolean()
    is_deleted = graphene.Boolean()


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
    location = graphene.String(required=True)
    is_available = graphene.Boolean(required=True)


class AddSectionInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    club_id = graphene.ID(required=True)
    sub_manager_id = graphene.ID(required=True)
    is_available = graphene.Boolean(required=True)


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
