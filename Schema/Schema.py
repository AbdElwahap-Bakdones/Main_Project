import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from test_app.models import Cars, Compani, PetModel
from graphene_django import DjangoListField


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


class CarsCategory(DjangoObjectType):
    class Meta:
        model = Cars
        fields = ('id', 'name', 'compani')

    extra_fields = graphene.String()

    def resolve_extra_fields(self, info):
        if self.color == 'red':
            return self.color
        return 'null'


class Pet(DjangoObjectType):
    class Meta:
        model = PetModel
        fields = ('id', 'kind', 'name')

    # @classmethod
    # def get_queryset(cls, queryset, info):
    #     # Filter out recipes that have no title
    #     return queryset.exclude(id__exact=1)


class PetModelMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.ID()
    print('00000000000')
    pet_filed = graphene.Field(Pet)

    @classmethod
    def mutate(cls, root, info, name, id):
        print(name, id)
        pet = PetModel.objects.filter(pk=id)
        print(pet.values_list())
        pet.update(name=name)

        return PetModelMutation(pet_filed=pet.get())


class Mutation(graphene.ObjectType):
    print('mutation')
    pet = PetModelMutation.Field()


class Query(graphene.ObjectType):
    hello = graphene.String(default_value='Hi!')
    all_Compani = relay.ConnectionField(
        QuestionConnection)  # graphene.List(CompaniCategory)
    Cars_by_nam = graphene.List(CarsCategory)
    Cars_by_Company = graphene.List(
        CarsCategory, compani=graphene.Int(required=True))
    all_Pet = DjangoListField(Pet)

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

    # def resolve_all_Pet(root, info):
    #     return PetModel.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)
