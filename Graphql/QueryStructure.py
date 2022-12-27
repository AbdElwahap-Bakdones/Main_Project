from rest_framework import status as status_code
import graphene


class Attributes():
    data = graphene.Field(object)
    message = graphene.String()
    status = graphene.Int()
    # test = graphene.String()


def MyReturn(instanse: object, data: object, message: str, code: status_code):
    return instanse(data=data, message=message, status=code)
