import graphene
from graphene_django import DjangoObjectType
from test_app.models import Cars, Compani


class CompaniCategory(DjangoObjectType):
    class Meta:
        model = Compani
        fields = ('id', 'name')


class CarsCategory(DjangoObjectType):
    class Meta:
        model = Cars
        fields = ('id', 'name', 'compani')


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    all_Compani = graphene.List(CompaniCategory)
    Cars_by_nam = graphene.Field(
        CarsCategory, name=graphene.String(required=True))
    Cars_by_Company = graphene.List(
        CarsCategory, compani=graphene.Int(required=True))

    def resolve_all_Compani(root, info):
        try:
            return Compani.objects.all()
        except:
            return Compani.DoesNotExist()

    def resolve_Cars_by_nam(root, info, name):
        print(name)
        try:
            return Cars.objects.get(name=name)
        except:
            return Compani.DoesNotExist()

    def resolve_Cars_by_Company(root, info, compani):
        print(compani)
        return Cars.objects.filter(compani=compani)


schema = graphene.Schema(query=Query)
