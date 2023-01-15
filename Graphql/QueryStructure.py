from rest_framework import status as status_code
from graphql.execution.base import ResolveInfo
from graphql.language.ast import Field, SelectionSet
from .Auth import permission

import graphene


class Attributes():
    data = graphene.Field(object)
    message = graphene.String()
    status = graphene.Int()
    # test = graphene.String()


def BadRequest(instanse: object, message='Bad Request'):
    return instanse(
        data=None, message=message,
        status=status_code.HTTP_400_BAD_REQUEST)


def NoPermission(instanse: object):
    return instanse(
        data=None, message='You do not have permission to complete the process',
        status=status_code.HTTP_403_FORBIDDEN)


def MyReturn(instanse: object, data: object, message: str, code: status_code):
    return instanse(data=data, message=message, status=code)


def NotFound(instanse: object):
    return instanse(
        data=None, message='Not found',
        status=status_code.HTTP_404_NOT_FOUND)


def OK(instanse: object, data=None):
    return instanse(
        data=data, message='OK',
        status=status_code.HTTP_200_OK)


def InternalServerError(instanse: object, message='server error'):
    return instanse(
        data=None, message=message,
        status=status_code.HTTP_500_INTERNAL_SERVER_ERROR)


def Created(instanse: object, data=None, message='Created !'):
    return instanse(data=data, message=message,
                    status=status_code.HTTP_201_CREATED)


class QueryFields(object):
    status = graphene.Int()
    message = graphene.String()
    data = graphene.AbstractType
    return_dict = {}

    # def __init__(self):
    #     print('init QueryFields')
    #     if len(QueryFields) > 50:
    #         last_user = list(QueryFields.return_dict)[-1]
    #         del QueryFields.return_dict[last_user]
    def clear():
        print('clear QueryFields')
        if len(QueryFields.return_dict) > 2:
            last_user = list(QueryFields.return_dict)[-1]
            del QueryFields.return_dict[last_user]

    def __chack_if_data_call_first(info: ResolveInfo) -> bool:
        if SelectionSet(Field(
                info.operation.selection_set.selections[0]).name.selection_set).selections.selections[0].name.value == 'data':
            return True
        return False

    def is_valide(info: ResolveInfo, user: object, operation: str) -> bool:
        QueryFields.clear
        if not permission.checkPermission(operation, user):
            QueryFields.__no_permission(user)
            return False
        if not QueryFields.__chack_if_data_call_first(info):
            return False
        return True

    def rise_error(user: object):
        return []

    def __no_permission(user: object):
        QueryFields.set_extra_data(
            user, status_code.HTTP_403_FORBIDDEN, 'you dont have permission')
        return []

    def set_extra_data(user: object, status: status_code, message: str):
        QueryFields.return_dict[user] = {}
        QueryFields.return_dict[user]['status'] = status
        QueryFields.return_dict[user]['message'] = message

    def resolve_status(root, info: ResolveInfo, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.__chack_if_data_call_first(info):
                return status_code.HTTP_400_BAD_REQUEST
            status = QueryFields.return_dict[user]['status']
            QueryFields.return_dict[user]['status'] = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            print('Error in resolve_status')
            print(str(e))
            status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
        return status

    def resolve_message(root, info: ResolveInfo, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.__chack_if_data_call_first(info):
                return 'plase call data first'
            message = QueryFields.return_dict[user]['message']
            QueryFields.return_dict[user]['message'] = 'INTERNAL_SERVER_ERROR'
        except Exception as e:
            print('Error in resolve_message')
            print(str(e))
            message = 'INTERNAL_SERVER_ERROR'
        return message

    def resolve_data(root, info: ResolveInfo, **kwargs):
        return []

    def NotFound(info: ResolveInfo):
        user = info.context.META['user']
        QueryFields.set_extra_data(
            user, status_code.HTTP_404_NOT_FOUND, 'not exists')
        return []

    def BadRequest(info: ResolveInfo):
        user = info.context.META['user']
        QueryFields.set_extra_data(
            user, status_code.HTTP_400_BAD_REQUEST, 'Bad Request')
        return []

    def ServerError(info: ResolveInfo, msg='Server Error'):
        user = info.context.META['user']
        QueryFields.set_extra_data(
            user, status_code.HTTP_500_INTERNAL_SERVER_ERROR, msg)
        return []

    def OK(info: ResolveInfo, data=[]):
        user = info.context.META['user']
        QueryFields.set_extra_data(
            user, status_code.HTTP_200_OK, 'OK')
        return data

    def queryAll(obj, info: ResolveInfo, permission):
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, permission):
            return QueryFields.rise_error(user)
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'OKK')
        return obj.objects.all()

    def queryGet(obj, info: ResolveInfo, permission, id):
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, permission):
            return QueryFields.rise_error(user)
        data = obj.objects.filter(id=id)
        if not data.exists():
            QueryFields.NotFound(info)

        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'okk')
        return data
