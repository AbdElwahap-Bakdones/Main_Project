import jwt
from core.models import User
from main_project.settings import SECRET_KEY, FunctionDonotNeedAuth
import graphene
from graphql import GraphQLError


def checkToken(info):
    try:
        if not 'HTTP_TOKEN' in info.context.META:
            raise GraphQLError({'errorname': 'donky', 'codeerror': 401})
        username = jwt.decode(
            info.context.META['HTTP_TOKEN'], SECRET_KEY, algorithms=['HS256'])
        user = User.objects.filter(username=username["username"])
        if user.exists():
            return {"user": user.first()}
        else:
            raise Exception(jwt.InvalidTokenError)
    except jwt.DecodeError or jwt.InvalidTokenError as e:
        raise Exception(e)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        if not info.operation.selection_set.selections[0].name.value in FunctionDonotNeedAuth:
            info.context.META.update(checkToken(info))

        # print(dict(info.context.META))
        # m= jwt.decode(info.context.META['HTTP_TOKEN'],'django-insecure-z@mx14w10q5&76myvh@5v+#bzz@eabj0mgnz6q3^9^iypw53l7',algorithms=['HS256'])
        # print(m)
        # print(info.context.user)
        # if info.operation.operation == 'mutation':
        #     print('mutation')
        # if info.operation.operation == 'query':
        #     print('query')
        return next(root, info, **args)
