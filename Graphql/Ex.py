from graphene.types.scalars import Scalar


class ObjectField(Scalar):  # to serialize error message from serializer
    @staticmethod
    def serialize(dt):
        return dt


class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject


# For mutation, use serializers

# creating subject
class CreateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)
    message = ObjectField()
    status = graphene.Int()

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        serializer = SubjectSerializer(data=kwargs)
        if serializer.is_valid():
            obj = serializer.save()
            msg = 'success'
        else:
            msg = serializer.errors
            obj = None
            print(msg)
        return cls(subject=obj, message=msg, status=200)


# Updating subject


class UpdateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectType)
    status = graphene.Int()
    message = ObjectField()

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        sub = Subject.objects.get(id=id)
        serializer = SubjectSerializer(sub, data=kwargs, partial=True)
        if serializer.is_valid():
            obj = serializer.save()
            msg = 'success'
        else:
            msg = serializer.errors
            obj = None
            print(msg)
        return cls(subject=obj, message=msg, status=200)


# Delete Subject


class DeleteSubject(graphene.Mutation):
    message = ObjectField()
    status = graphene.Int()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        c = Subject.objects.get(id=id)
        c.delete()
        return cls(message='success', status=200)


class Mutation(graphene.ObjectType):
    create_subject = CreateSubject.Field()
    update_subject = UpdateSubject.Field()
    delete_subject = DeleteSubject.Field()

# Query is normal.


class Query(graphene.ObjectType):
    subject = graphene.Field(
        SubjectType, id=graphene.Int(), slug=graphene.String())

    subjects = graphene.List(SubjectType)

    def resolve_subject(self, info, id=None, slug=None):
        if id:
            return Subject.objects.get(id=id)
        if slug:
            return Subject.objects.get(slug=slug)

    def resolve_subjects(self, info, **kwargs):
        return Subject.objects.all()
 #########################################

 #########################################
