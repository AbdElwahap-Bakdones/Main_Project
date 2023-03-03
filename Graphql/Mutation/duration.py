from ..ModelsGraphQL import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from ..ModelsGraphQL import typeobject, inputtype
from .. import QueryStructure
import datetime
from graphene_django import DjangoObjectType
from graphene import relay
from rest_framework import status as status_code


class AddDurationList(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.DurationObjectType)

    class Arguments:
        data = inputtype.AddDurationInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_stadium", user):
                return QueryStructure.NoPermission(self)
            if QueryStructure.QueryFields.user_type(user, models.Manager):
                stadium = models.Stadium.objects.filter(section_id__club_id__manager_id__user_id=user,
                                                        id=kwargs["data"]["stad_id"], is_deleted=False)
            else:
                stadium = models.Stadium.objects.filter(section_id__sub_manager_id__user_id=user,
                                                        id=kwargs["data"]["stad_id"], is_deleted=False)
            if not stadium.exists():
                return QueryStructure.BadRequest(self, message="stadium not found")
            if not over(kwargs["data"]["duration"]):
                return QueryStructure.BadRequest(self, message="This time overlaps with others")

            checkOverlap = all([CheckOverlap(
                i["start_time"], i["end_time"], kwargs["data"]["stad_id"]) for i in kwargs["data"]["duration"]])
            if not checkOverlap:
                return QueryStructure.BadRequest(self, message="This time overlaps with others in database")
            for i in kwargs["data"]["duration"]:
                dataDuration = {"stad_id": kwargs["data"]["stad_id"],
                                "start_time": i["start_time"], "end_time": i["end_time"], "is_available": i["is_available"], "price": i["price"]}
                seria = serializer.DurationSerializer(data=dataDuration)
                if seria.is_valid():
                    seria.validated_data
                    seria.save()
            return QueryStructure.OK(self, data=seria.save())
        except Exception as e:
            return QueryStructure.InternalServerError(self, message=str(e))


class UpdateDurationList(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.DurationObjectType)

    class Arguments:
        data = inputtype.UpdateDurationInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_stadium", user):
                return QueryStructure.NoPermission(self)
            durationNewList = kwargs["data"]["duration"]
            if not over(durationNewList):
                return QueryStructure.BadRequest(self, message="This time overlaps with others")
            if QueryStructure.QueryFields.user_type(user, models.Manager):
                duration = models.Duration.objects.filter(
                    stad_id=kwargs["data"]["stad_id"], stad_id__section_id__club_id__manager_id__user_id=user, is_deleted=False)
            else:
                duration = models.Duration.objects.filter(
                    stad_id=kwargs["data"]["stad_id"], stad_id__section_id__sub_manager_id__user_id=user, is_deleted=False)
            if not duration.exists():
                return QueryStructure.BadRequest(self, message="the staduim not found or you not have permission on this staduim ")
            if len(durationNewList) != duration.count():
                return QueryStructure.BadRequest(self, message="The number of new data must equal the number of old data")
            for i in range(len(durationNewList)):
                dd = duration.get(pk=duration[i].pk)
                dd.start_time = durationNewList[i]["start_time"]
                dd.start_time = durationNewList[i]["start_time"]
                dd.end_time = durationNewList[i]["end_time"]
                dd.is_available = durationNewList[i]["is_available"]
                dd.price = durationNewList[i]["price"]
                dd.save()
            return QueryStructure.OK(self, data=duration.last())
        except Exception as e:
            return QueryStructure.InternalServerError(self, message=str(e))


class DeleteDurationList(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.DurationObjectType)

    class Arguments:
        data = inputtype.DeleteDurationInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_stadium", user):
                return QueryStructure.NoPermission(self)
            if checkPermission("core.add_club", user):
                userType = "manager"
            else:
                userType = "subManager"
            data = kwargs['data']
            if data['id_list'] == []:
                return QueryStructure.BadRequest(self, message="the list is empty")
            for i in data['id_list']:
                if userType == "manager":
                    duration_object = models.Duration.objects.filter(stad_id__section_id__club_id__manager_id__user_id=user,
                                                                     id=i, is_deleted=False)
                else:
                    duration_object = models.Duration.objects.filter(stad_id__section_id__sub_manager_id__user_id=user,
                                                                     id=i, is_deleted=False)
            if not duration_object.exists():
                return QueryStructure.BadRequest(self, message="the duration has ID :"+str(i)+" is not found")
            for i in data['id_list']:
                duration_object = models.Duration.objects.filter(
                    id=i, is_deleted=False)
                seria = serializer.DurationSerializer(
                    duration_object.first(), data={"is_deleted": True}, partial=True)
                if seria.is_valid():
                    seria.validated_data
                    seria.save()
            return QueryStructure.OK(self, data=seria.save())
        except Exception as e:
            print(e)
            msg = str(e)
            data = None
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return QueryStructure.MyReturn(instanse=self, data=data, message=msg, code=status)


def CheckOverlap(start, end, stad_id):
    j = models.Duration.objects.filter(stad_id__id=stad_id, is_deleted=False)
    for i in j:
        if i.start_time <= start < i.end_time or i.start_time < end <= i.end_time:
            return False
    return True


def CheckUpdateOverlap(id, start, end, stad_id):
    j = models.Duration.objects.filter(stad_id__id=stad_id, is_deleted=False)
    for i in j:
        if int(id) == i.pk:
            continue
        if i.start_time <= start < i.end_time or i.start_time < end <= i.end_time:
            return False
    return True


def over(lists):
    for i in lists:
        for j in lists:
            if i == j:
                continue
            if j['start_time'] <= i['start_time'] < j['end_time'] or j['start_time'] < i['end_time'] <= j['end_time']:
                return False
    return True
