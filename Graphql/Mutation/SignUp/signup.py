import graphene
from core import serializer
from ...ModelsGraphQL import typeobject, inputtype
from rest_framework import status as status_code
from ... import QueryStructure
from django.contrib.auth.models import Group


class SignUpPlayer(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.PlayerObjectType)

    class Arguments:
        data = inputtype.PlayerInput()

    @classmethod
    def mutate(self, root, info, **kargs):
        status = status_code.HTTP_400_BAD_REQUEST
        user = None
        player = None
        msg = {}
        user_error = {}
        player_error = {}
        try:
            user_data = kargs['data'].pop('user')  # extract data
            data = kargs['data']  # extract data
            data['user_id'] = 41  # Set an initial user_id vlaue
            user_data['username'] = user_data['first_name'] + '@' + \
                user_data['last_name']  # define username as first_name@last_name

            # add User via serializer   &  add player via serializer
            seria_user = serializer.UserSerializer(data=user_data)
            seria_player = serializer.PlayerSerializer(data=data)
            is_valid = seria_user.is_valid() * seria_player.is_valid()
            if is_valid:
                seria_user.validated_data
                user = seria_user.save()
                # Set a correct user_id value
                data['user_id'] = user.pk
                seria_player = serializer.PlayerSerializer(data=data)
                seria_player.is_valid(
                    raise_exception='internal servre Error')
                player = seria_player.save()
                groups = Group.objects.get(id=1)
                groups.user_set.add(user)
                status = status_code.HTTP_201_CREATED
                msg = 'ok'
            else:
                user_error = dict(seria_user.errors)
                player_error = dict(seria_player.errors)
                user_error.update(player_error)
                msg = user_error
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in SignUpPlayer ')
            print(e)
            user = None
            player = None
            msg = e
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        # self(user=user, player=player, message=msg, status=status)
        return QueryStructure.MyReturn(self, player, msg, status)


class SignUpManager(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.ManagerObjectType)

    class Arguments:
        data = inputtype.ManagerInput()

    @classmethod
    def mutate(self, root, info, **kargs):
        status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        user = None
        manager = None
        msg = {}
        user_error = {}
        manager_error = {}
        try:
            print(kargs)
            user_data = kargs['data'].pop('user')  # extract data
            print(kargs)
            data = kargs['data']  # extract data
            data['user_id'] = 41  # Set an initial user_id vlaue
            user_data['username'] = user_data['first_name'] + '@' + \
                user_data['last_name']  # define username as first_name$last_name

            # add User via serializer   &  add manager via serializer
            seria_user = serializer.UserSerializer(data=user_data)
            seria_manager = serializer.ManagerSerializer(data=data)
            is_valid = seria_user.is_valid() * seria_manager.is_valid()
            if is_valid:
                seria_user.validated_data
                user = seria_user.save()
                # Set a correct user_id value
                data['user_id'] = user.pk
                seria_manager = serializer.ManagerSerializer(
                    data=data)
                seria_manager.is_valid(
                    raise_exception='internal servre Error')
                manager = seria_manager.save()
                groups = Group.objects.get(id=3)
                groups.user_set.add(user)
                # cheack if manager is subManager
                # self.create_subManager(kargs['is_submanager'], data)
                status = 200
                msg = 'ok'
            else:
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
        return QueryStructure.MyReturn(self, manager, msg, status)

    def create_subManager(is_submanager: bool, user_id: int):
        seria_subManager = serializer.SubManagerSerializer(data=user_id)
        if is_submanager and seria_subManager.is_valid():
            seria_subManager.save()


class SignUpSubManager(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.SubManagerObjectType)

    class Arguments:
        data = inputtype.SubManagerInput()

    @classmethod
    def mutate(self, root, info, **kargs):
        status = status_code.HTTP_400_BAD_REQUEST
        user = None
        subManager = None
        msg = {}
        user_error = {}
        subManager_error = {}
        try:
            print(kargs)
            user_data = kargs['data'].pop(
                'user')  # extract data
            data = kargs['data']  # extract data
            data['user_id'] = 41  # Set an initial user_id vlaue
            user_data['username'] = user_data['first_name'] + '@' + \
                user_data['last_name']  # define username as first_name@last_name
            # add User via serializer   &  add subManager via serializer
            seria_user = serializer.UserSerializer(data=user_data)
            seria_subManager = serializer.SubManagerSerializer(
                data=data)
            is_valid = seria_user.is_valid() * seria_subManager.is_valid()
            if is_valid:
                seria_user.validated_data
                user = seria_user.save()
                user.groups
                # Set a correct user_id value
                data['user_id'] = user.pk
                seria_subManager = serializer.SubManagerSerializer(
                    data=data)
                seria_subManager.is_valid(
                    raise_exception='internal servre Error')
                subManager = seria_subManager.save()
                status = status_code.HTTP_201_CREATED
                msg = 'ok'
            else:
                print('else')
                user_error = dict(seria_user.errors)
                subManager_error = dict(seria_subManager.errors)
                user_error.update(subManager_error)
                msg = user_error
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            user = None
            subManager = None
            msg = e
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(self, subManager, msg, status)
