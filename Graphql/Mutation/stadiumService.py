from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from .. import QueryStructure
from rest_framework import status as status_code


class AddServicesForStadiums(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.StadiumServiceObjectType)

    class Arguments:
        data = inputtype.AddStadiumServiceInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = models.User(info.context.META["user"])
            if not checkPermission("core.add_stadiumservice", user.pk):
                return QueryStructure.NoPermission(self)
            if checkPermission("core.add_club", user.pk):
                userType = "manager"
            else:
                userType = "subManager"
            data = kwargs["data"]
            if userType == "manager":
                checkdata = models.Stadium.objects.filter(
                    section_id__club_id__manager_id__user_id=user, id=data["stad_id"], is_deleted=False)
            else:
                checkdata = models.Stadium.objects.filter(
                    section_id__sub_manager_id__user_id=user, id=data["stad_id"], is_deleted=False)
            if not checkdata.exists():
                return QueryStructure.BadRequest(self, message="the staduim not found")
            seria = serializer.StadiumServiceSerializer(
                data=kwargs["data"])
            if seria.is_valid():
                seria.validated_data
                data = seria.save()
                return QueryStructure.Created(self, data=data)
            else:
                msg = seria.errors
                data = None
                status = status_code.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            print('Error in AddClub :')
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)


class ModificationsToStadiumServices(graphene.Mutation):
    stadiumService = graphene.Field(typeobject.StadiumServiceObjectType)
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        stad_id = graphene.ID(required=True)
        service_id = graphene.ID(required=True)
        is_available = graphene.Boolean()

    @classmethod
    def mutate(self, root, info, **kwargs):
        checkPermission("core.change_stadiumservice", info)
        sub = models.StadiumService.objects.filter(
            stad_id=kwargs["stad_id"], service_id=kwargs["service_id"]).first()
        seria = serializer.StadiumServiceSerializer(sub,
                                                    data=kwargs, partial=True)
        if seria.is_valid():
            seria.validated_data
            msg = seria.errors
            status = 200
            stadiumService = seria.save()
        else:
            msg = seria.errors
            stadiumService = None
            status = 400
        return self(stadiumService=stadiumService, message=msg, status=status)
