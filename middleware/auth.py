
import jwt


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        # print(dict(info.context.META))
        # token= jwt.decode(info.context.META['HTTP_TOKEN'],'django-insecure-z@mx14w10q5&76myvh@5v+#bzz@eabj0mgnz6q3^9^iypw53l7',algorithms=['HS256'])
        # print(token)
        # print(info.context.user)
        # if info.operation.operation == 'mutation':
        #     print('mutation')
        # if info.operation.operation == 'query':
        #     print('query')
        return next(root, info, **args)
