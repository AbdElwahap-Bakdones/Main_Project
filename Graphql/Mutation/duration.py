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


class DurationInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    start_time = graphene.Time(required=True)
    end_time = graphene.Time(required=True)
    time_reservation = graphene.Time(required=True)


class AddDuration(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.DurationObjectType)

    class Arguments:
        data = DurationInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        user = info.context.META["user"]
        if not checkPermission("core.add_duration", user):
            return QueryStructure.NoPermission(self)
        start = kwargs["data"]["start_time"]
        end = kwargs["data"]["end_time"]
        range_time = kwargs["data"]["time_reservation"]
        if not CheckOverlap(start, end):
            msg = "problem time"
            duration = None
            status = 400
            return self(data=duration, message=msg, status=status)
        stadium = models.Stadium.objects.filter(
            id=kwargs["data"]["stad_id"])
        if not stadium.exists():
            msg = "not exists"
            duration = None
            status = 404
            return self(data=duration, message=msg, status=status)
        stadiumtype = stadium.filter(type_id__id=4)
        if stadiumtype.exists():
            msg = "This API cannot be used for the swim type"
            duration = None
            status = 400
            return self(data=duration, message=msg, status=status)
        m = sturctTime(start, end, range_time)
        k = (m["end"]-m["start"])/m["range_time"]
        for i in range(int(k)):
            # if m["end"]-m["start"] < m["range_time"]:
            #     break
            old = datetime.datetime(
                2021, 8, 22, start.hour, start.minute, start.second)
            newtime = datetime.timedelta(minutes=m["range_time"])
            change = old+newtime
            dd = models.Duration.objects.create(stad_id=stadium.first(), start_time=start,
                                                end_time=change)
            dd.save()
            start = change
        return QueryStructure.MyReturn(instanse=self, data=models.Duration.objects.filter(stad_id__id=kwargs["data"]["stad_id"]).last(), message="ok", code=200)


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
            if checkPermission("core.add_club", user):
                userType = "manager"
            else:
                userType = "subManager"
            if userType == "manager":
                stadium = models.Stadium.objects.filter(section_id__club_id__manager_id__user_id=user,
                                                        id=kwargs["data"]["stad_id"])
            else:
                stadium = models.Stadium.objects.filter(section_id__sub_manager_id__user_id=user,
                                                        id=kwargs["data"]["stad_id"])
            if not stadium.exists():
                return QueryStructure.BadRequest(self, message="stadium not found")
            # checkOverlap = all([CheckOverlap(
            #     i["start_time"], i["end_time"], kwargs["data"]["stad_id"]) for i in kwargs["data"]["time"]])
            # if not checkOverlap:
            #     return QueryStructure.BadRequest(self, message="This time overlaps with others")
            for i in kwargs["data"]["time"]:
                dataDuration = {"stad_id": kwargs["data"]["stad_id"],
                                "start_time": i["start_time"], "end_time": i["end_time"], "is_available": i["is_available"]}
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
            if checkPermission("core.add_club", user):
                userType = "manager"
            else:
                userType = "subManager"
            # checkOverlap = all([CheckOverlap(
            #     i["start_time"], i["end_time"], kwargs["data"]["stad_id"]) for i in kwargs["data"]["duration"]])
            # if not checkOverlap:
            #     return QueryStructure.BadRequest(self, message="This time overlaps with others")
            for i in kwargs["data"]["duration"]:
                if userType == "manager":
                    sub = models.Duration.objects.filter(stad_id__section_id__club_id__manager_id__user_id=user,
                                                         id=i['id'])
                else:
                    sub = models.Duration.objects.filter(stad_id__section_id__sub_manager_id__user_id=user,
                                                         id=i['id'])
                if not sub.exists():
                    return QueryStructure.NotFound(self)
            for i in kwargs["data"]["duration"]:
                sub = models.Duration.objects.filter(
                    id=i['id'])
                dataDuration = {
                    "start_time": i["start_time"], "end_time": i["end_time"], "is_available": i["is_available"]}
                seria = serializer.DurationSerializer(
                    sub.first(), data=dataDuration, partial=True)
                if seria.is_valid():
                    seria.validated_data
                    seria.save()
            return QueryStructure.OK(self, data=seria.save())
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


def cheackTime(start, end, range_time):
    if end < start:
        return False
    t1 = start.hour*60+start.minute
    t2 = end.hour*60+end.minute
    t3 = range_time.hour*60+range_time.minute
    t = t2-t1
    if t < t3:
        return False
    return True


def CheckOverlap(start, end, stad_id):
    j = models.Duration.objects.filter(stad_id__id=stad_id, is_deleted=False)
    for i in j:
        if i.start_time <= start < i.end_time or i.start_time < end <= i.end_time:
            return False
    return True


li = [{"id": 1, "startTime": "16:30:00", "endTime": "18:00:00", "isAvailable": True}, {"id": 2, "startTime": "18:30:00",
                                                                                       "endTime": "20:00:00", "isAvailable": True}, {"id": 3, "startTime": "18:30:00", "endTime": "20:00:00", "isAvailable": True}]


def over(lists):
    for i in range(len(lists)-1):

        print(lists[i+1]['startTime'])


over(li)


def sturctTime(start, end, range_time):
    return {"start": start.hour*60, "end": end.hour*60, "range_time": range_time.hour*60}


def convertHourToMinute(hour):
    return hour*60


# class UpdateDuration(graphene.Mutation, QueryStructure.Attributes):
#     data = graphene.Field(typeobject.DurationObjectType)

#     class Arguments:
#         id = graphene.ID(required=True)
#         name = graphene.String()
#         section_id = graphene.ID()
#         type_id = graphene.ID()
#         size = graphene.Float()
#         is_available = graphene.Boolean()
#         has_legua = graphene.Boolean()

#     @classmethod
#     def mutate(self, root, info, id, **kwargs):
#         checkPermission("core.change_Duration", info)
#         sub = models.Duration.objects.get(id=id)
#         seria = serializer.DurationSerializer(sub,
#                                               data=kwargs, partial=True)
#         if seria.is_valid():
#             seria.validated_data
#             msg = seria.errors
#             status = 200
#             Duration = seria.save()
#         else:
#             msg = seria.errors
#             Duration = None
#             status = 400
#         return self(Duration=Duration, message=msg, status=status)
