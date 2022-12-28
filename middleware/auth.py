

class AuthorizationMiddleware(object):
    def __init__(self):
        self.authorized = False

    def resolve(self, next, root, info, **args):

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
