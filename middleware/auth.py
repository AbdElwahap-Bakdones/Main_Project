import jwt
from core.models import User, Rule
from main_project.settings import SECRET_KEY, FunctionDonotNeedAuth
import graphene
from graphql import GraphQLError
from graphql.execution.base import ResolveInfo
from graphql.language.ast import*


def decode_token(token: str) -> User:
    username = jwt.decode(
        token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.filter(username=username["username"])
    if user.exists():
        return {"user": user.first()}
    else:
        raise Exception(jwt.InvalidTokenError)


class AuthorizationMiddleware(object):
    def __init__(self):
        self.authorized = False

    def checkToken(self, next, root, info, args):
        try:
            if not 'HTTP_TOKEN' in info.context.META:
                return GraphQLError('message')
            token = info.context.META['HTTP_TOKEN']
            info.context.META.update(decode_token(token))
            self.authorized = True
            return next(root, info, **args)

        except jwt.DecodeError or jwt.InvalidTokenError as e:
            print(e)
            return None

    def resolve(self, next, root, info, **args):
        return next(root, info, **args)

        operation = info.operation.selection_set.selections[0].name.value
        if not operation in FunctionDonotNeedAuth:
            return self.checkToken(next=next, root=root, info=info, args=args)
        if self.authorized or operation in FunctionDonotNeedAuth:
            return next(root, info, **args)

# m= jwt.decode(info.context.META['HTTP_TOKEN'],'django-insecure-z@mx14w10q5&76myvh@5v+#bzz@eabj0mgnz6q3^9^iypw53l7',algorithms=['HS256'])
    # print(m)
    # print(info.context.user)
    # if info.operation.operation == 'mutation':
    #     print('mutation')
    # if info.operation.operation == 'query':
    #     print('query')
    # print(info.operation.selection_set.selections[0].name.value)


'''def not_auth(self, info: ResolveInfo):
    info.field_name = 'hello'
    info.field_asts = [Field(alias=None, name=Name(value='hello'), arguments=[], directives=[], selection_set=SelectionSet(selections=[Field(alias=None, name=Name(
        value='status'), arguments=[], directives=[], selection_set=None), Field(alias=None, name=Name(value='message'), arguments=[], directives=[], selection_set=None)]))]
    info.parent_type = 'Query'
    info.fragments = {}
    info.root_value = None
    info.operation = OperationDefinition(operation='query', name=None, variable_definitions=[], directives=[], selection_set=SelectionSet(selections=[Field(alias=None, name=Name(value='hello'), arguments=[], directives=[], selection_set=SelectionSet(
        selections=[Field(alias=None, name=Name(value='status'), arguments=[], directives=[], selection_set=None), Field(alias=None, name=Name(value='message'), arguments=[], directives=[], selection_set=None)]))]))
    info.variable_values = {}
    info.path = ['hello', 'message']
    return info'''
