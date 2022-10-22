import graphene
from graphene_django import DjangoObjectType
from test_app.models import Cars, Compani, PetModel


class CompaniCategory(DjangoObjectType):
    class Meta:
        model = Compani
        fields = ('id', 'name')
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return self.id


class CarsCategory(DjangoObjectType):
    class Meta:
        model = Cars
        fields = ('id', 'name', 'compani')

        extra_fields = graphene.String()

        def resolve_extra_fields(self, info):
            return self


class Pet(DjangoObjectType):
    class Meta:
        model = PetModel
        fields = ('id', 'kind')


class Query(graphene.ObjectType):
    hello = graphene.String(default_value='Hi!')
    all_Compani = graphene.List(CompaniCategory)
    Cars_by_nam = graphene.List(CarsCategory)
    Cars_by_Company = graphene.List(
        CarsCategory, compani=graphene.Int(required=True))
    all_pet = graphene.List(Pet)

    def resolve_all_Compani(root, info):
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


schema = graphene.Schema(query=Query)
