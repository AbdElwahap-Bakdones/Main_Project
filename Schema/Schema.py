from time import time as timer
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from test_app.models import Cars, Compani, PetModel
from graphene_django import DjangoListField
from graphene_django.rest_framework.mutation import SerializerMutation
from test_app import serializer as testappSerializer
from rx import Observable
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from core.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import login_required
from http import HTTPStatus
import jwt


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()  # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()
    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class CompaniCategory(DjangoObjectType):
    class Meta:
        model = Compani
        fields = ('id', 'name')
        interfaces = (relay.Node,)
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class QuestionConnection(relay.Connection):
    class Meta:
        node = CompaniCategory


class Pet(DjangoObjectType):
    class Meta:
        model = PetModel
        fields = ('id', 'name')
        interfaces = (relay.Node,)


class PetRelay(relay.Connection):
    class Meta:
        node = Pet


class CarsCategory(DjangoObjectType):
    class Meta:
        model = Cars
        fields = ('id', 'name', 'compani')

    extra_fields = graphene.String()

    def resolve_extra_fields(self, info):
        if self.color == 'red':
            return self.color
        return 'null'

    # @classmethod
    # def get_queryset(cls, queryset, info):
    #     # Filter out recipes that have no title
    #     return queryset.exclude(id__exact=1)


# class PetModelMutation(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         id = graphene.ID()
#     print('00000000000')
#     pet_filed = graphene.Field(Pet)

#     @classmethod
#     def mutate(cls, root, info, name, id):
#         print(name, id)
#         pet = PetModel.objects.filter(pk=id)
#         print(pet.values_list())
#         pet.update(name=name)

#         return PetModelMutation(pet_filed=pet.get())


class Query(UserQuery, MeQuery, graphene.ObjectType):
    token_auth = mutations.ObtainJSONWebToken.Field()

    hello = graphene.String(default_value='Hi!')
    all_Compani = relay.ConnectionField(
        QuestionConnection)  # graphene.List(CompaniCategory)
    Cars_by_nam = graphene.List(CarsCategory)
    Cars_by_Company = graphene.List(
        CarsCategory, compani=graphene.Int(required=True))
    #all_Pet = DjangoListField(Pet)
    all_Pet = relay.ConnectionField(PetRelay)

    def resolve_hello(root, info, **kwargs):
        print(dict(info.context.META))
        print(info.context.user.is_authenticated)
        if info.context.user.is_authenticated:
            return 'abd'
        print('nooo')
        return 'ghaith'

    def resolve_all_Compani(root, info, **kwargs):
        try:

            return Compani.objects.all()
        except:
            return Compani.DoesNotExist()

    def resolve_Cars_by_nam(root, info):
        try:
            return Cars.objects.all()
        except:
            return Compani.DoesNotExist()

    def resolve_Cars_by_Company(root, info, compani):
        print(compani)

        return Cars.objects.filter(compani=compani)

    def resolve_all_Pet(root, info):
        return PetModel.objects.all()


# serilizer
class PetType(DjangoObjectType):
    class Meta:
        model = PetModel


class CreatePet(graphene.Mutation):
    pet = graphene.Field(PetType)
    message = testappSerializer.ObjectField()
    status = graphene.Int()
    verify_token = mutations.VerifyToken.Field()

    class Arguments:

        name = graphene.String(required=True)

    @classmethod
    def mutate(self, root, info, **kwargs):
        user = User(info.context.user)
        print('enddddddddd')
        print(info.context.user.is_authenticated)

        # print(dict(info.context.META))
        serializer = testappSerializer.PetSerSerializer(data=kwargs)
        if serializer.is_valid():
            obj = serializer.save()
            msg = 'success'

        else:
            msg = 'serializer.errors'
            obj = None

        return self(pet=obj, message=msg, status=HTTPStatus.CREATED)


class UpdataPet(graphene.Mutation):
    pet = graphene.Field(PetType)
    status = graphene.Int()
    message = testappSerializer.ObjectField()

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    @classmethod
    def mutate(self, root, info, id, **kwargs):
        pt = PetModel.objects.get(id=id)
        serializer = testappSerializer.PetSerSerializer(
            instance=pt, data=kwargs)
        if serializer.is_valid():
            obj = serializer.save()
            msg = 'updated'
        else:
            msg = serializer.errors
            obj = None
            print(msg)
        return self(pet=obj, message=msg, status=200)


class DeletePet(graphene.Mutation):
    message = testappSerializer.ObjectField()
    status = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    def mutate(self, root, info, id, **kwargs):
        pt = PetModel.objects.get(id=id)
        pt.delete()
        return self(message='success', status=200)


class Mutation (AuthMutation, graphene.ObjectType):
    # print('mutation')
    create_pet = CreatePet.Field()
    update_pet = UpdataPet.Field()
    deltee_pet = DeletePet.Field()

    # @mutation.field("replyUpdate")
    # def reply_update(_obj, info, reply):
    #     """Resolver for reply update."""

    #     request: ASGIRequest = info.context["request"]
    #     print('12312313123')


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


def check_token(token: str) -> map:
    try:
        m = jwt.decode(token, 'Abd', algorithms=['HS256'])
        id = m['id']
        email = m['email']
        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
            return {'state': True, 'id': id, 'email': email, 'user_obj': user_obj}
        raise Exception('Invalid token')
    except Exception as e:
        print('Error checkToken functions')
        print(e)
        return {'state': False}


# class AuthorizationMiddleware(object):
#     def resolve(self, next, root, info, **args):
#         # print(dict(info.context.META))
#         print('0000000000')
#         print(info.context.user)
#         if info.operation.operation == 'mutation':
#             print('mutation')
#         if info.operation.operation == 'query':
#             print('query')
#         return next(root, info, **args)


schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)
