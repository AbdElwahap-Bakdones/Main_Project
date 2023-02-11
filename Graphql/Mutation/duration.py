from ..ModelsGraphQL import typeobject
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from ..ModelsGraphQL import typeobject, inputtype
from .. import QueryStructure
import datetime
from graphene_django import DjangoObjectType
from graphene import relay


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
        print(dueationlist(start, end))
        if not cheackTime(start, end, range_time):
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


class time(graphene.InputObjectType):
    start_time = graphene.Time()
    end_time = graphene.Time()


class DurationsInput(graphene.InputObjectType):
    stad_id = graphene.ID(required=True)
    time = graphene.List(time)


class AddDurationlist(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.DurationObjectType)

    class Arguments:
        data = DurationsInput()

    @classmethod
    def mutate(self, root, info, **kwargs):
        user = info.context.META["user"]
        if not checkPermission("core.add_duration", user):
            return QueryStructure.NoPermission(self)
        stadium = models.Stadium.objects.filter(
            id=kwargs["data"]["stad_id"])
        if not stadium.exists():
            msg = "stadium not found"
            duration = None
            status = 404
            return self(data=duration, message=msg, status=status)
        for i in kwargs["data"]["time"]:
            if not dueationlist(i["start_time"], i["end_time"], kwargs["data"]["stad_id"]):
                msg = "This time overlaps with others"
                duration = None
                status = 400
                return self(data=duration, message=msg, status=status)
            dataDuration = {"stad_id": kwargs["data"]["stad_id"],
                            "start_time": i["start_time"], "end_time": i["end_time"], "is_available": True}
            seria = serializer.ClubSerializer(data=dataDuration)
            if seria.is_valid():
                seria.validated_data
                msg = seria.errors
                status = 200
                data = seria.save()
                return self(data=data, message=msg, status=status)
            else:
                msg = seria.errors
                data = None
                status = 400
                return self(data=data, message=msg, status=status)
        return QueryStructure.MyReturn(instanse=self, data=models.Duration.objects.filter(stad_id__id=kwargs["data"]["stad_id"]).last(), message="ok", code=200)


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


def dueationlist(start, end, stad_id):
    j = models.Duration.objects.filter(stad_id__id=stad_id)
    for i in j:
        if i.start_time <= start < i.end_time or i.start_time < end <= i.end_time:
            return False
    return True


def sturctTime(start, end, range_time):
    return {"start": start.hour*60, "end": end.hour*60, "range_time": range_time.hour*60}


def convertHourToMinute(hour):
    return hour*60
# class UpdateDuration(graphene.Mutation):
#     Duration = graphene.Field(typeobject.DurationObjectType)
#     message = graphene.String()
#     status = graphene.Int()

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
