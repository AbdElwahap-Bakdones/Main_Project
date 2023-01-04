
import graphene


class AddClubInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    location_lat = graphene.String(required=True)
    location_long = graphene.String(required=True)
    is_available = graphene.Boolean(default=True)


class InputUpdateClub(graphene.InputObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    is_available = graphene.Boolean(required=True)
    is_deleted = graphene.Boolean(required=True)


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


class Ghaith(graphene.InputObjectType):
    user = graphene.Field(UserInput)
    field = graphene.String(requierd=False)
