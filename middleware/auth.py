
class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        # print(dict(info.context.META))
        # print('0000000000')
        # print(info.context.user)
        # if info.operation.operation == 'mutation':
        #     print('mutation')
        # if info.operation.operation == 'query':
        #     print('query')
        return next(root, info, **args)
