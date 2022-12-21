import graphene
from ...graphql_models import UserInput, UserModel, PlayerInput, PlayerModel, ManagerModel, ManagerInput
from core import serializer
from rest_framework import status as status_code


class SignUpPlayer(graphene.Mutation):
    user = graphene.Field(UserModel)
    player = graphene.Field(PlayerModel)
    message = graphene.String()
    status = graphene.Int()
    #

    class Arguments:
        user_data = UserInput()
        player_data = PlayerInput()

    @classmethod
    def mutate(self, root, info, **kargs):
        status = status_code.HTTP_400_BAD_REQUEST
        user = None
        player = None
        msg = {}
        user_error = {}
        player_error = {}
        try:
            user_data = kargs['user_data']  # extract data
            player_data = kargs['player_data']  # extract data
            player_data['user_id'] = 1  # Set an initial user_id vlaue
            user_data['username'] = user_data['first_name'] + '@' + \
                user_data['last_name']  # define username as first_name@last_name

            # add User via serializer   &  add player via serializer
            seria_user = serializer.UserSerializer(data=user_data)
            seria_player = serializer.PlayerSerializer(data=player_data)
            is_valid = seria_user.is_valid() * seria_player.is_valid()
            if is_valid:
                seria_user.validated_data
                user = seria_user.save()
                # Set an correct user_id value
                player_data['user_id'] = user.pk
                seria_player = serializer.PlayerSerializer(data=player_data)
                seria_player.is_valid(
                    raise_exception='internal servre Error')
                player = seria_player.save()
                status = status_code.HTTP_201_CREATED
                msg = 'ok'
            else:
                print('else')
                user_error = dict(seria_user.errors)
                player_error = dict(seria_player.errors)
                user_error.update(player_error)
                msg = user_error
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            user = None
            player = None
            msg = e
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return self(user=user, player=player, message=msg, status=status)


class SignUpManager(graphene.Mutation):
    user = graphene.Field(UserModel)
    manager = graphene.Field(ManagerModel)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        user_data = UserInput()
        manager_data = ManagerInput()

    @classmethod
    def mutate(self, root, info, **kargs):
        status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        user = None
        manager = None
        msg = {}
        user_error = {}
        manager_error = {}
        try:
            user_data = kargs['user_data']  # extract data
            manager_data = kargs['manager_data']  # extract data
            manager_data['user_id'] = 1  # Set an initial user_id vlaue
            user_data['username'] = user_data['first_name'] + '@' + \
                user_data['last_name']  # define username as first_name$last_name

            # add User via serializer   &  add manager via serializer
            seria_user = serializer.UserSerializer(data=user_data)
            seria_manager = serializer.ManagerSerializer(data=manager_data)
            is_valid = seria_user.is_valid() * seria_manager.is_valid()
            if is_valid:
                seria_user.validated_data
                user = seria_user.save()
                # Set an correct user_id value
                manager_data['user_id'] = user.pk
                seria_manager = serializer.ManagerSerializer(
                    data=manager_data)
                seria_manager.is_valid(
                    raise_exception='internal servre Error')
                manager = seria_manager.save()
                status = 200
                msg = 'ok'
            else:
                print('else')
                user_error = dict(seria_user.errors)
                manager_error = dict(seria_manager.errors)
                user_error.update(manager_error)
                msg = user_error
                status = 400
        except Exception as e:
            user = None
            manager = None
            msg = e
            status = 400
        return self(user=user, manager=manager, message=msg, status=status)
