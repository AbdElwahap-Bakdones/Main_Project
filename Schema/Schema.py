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
    Cars_by_nam = graphene.Field(Cars, name=graphene.String(required=True))
    Cars_by_Company = graphene.Field(
        Cars, Company_name=graphene.String(required=True))

    def resolve_all_Compani(root, info):
        try:
            return Compani.objects.all()
        except:
            return Compani.DoesNotExist()


schema = graphene.Schema(query=Query)
