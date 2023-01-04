

class ManagerCategory(DjangoObjectType):

    class Meta:
        model = Manager
        fields = ['user_id']
        interfaces = (relay.Node,)


class ManagerConnection(relay.Connection):

    class Meta:
        node = ManagerCategory


class QQ(ObjectType, QueryFields):
    data = relay.ConnectionField(ManagerConnection)

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if permission.checkPermission('aa', user):
            return QueryFields.no_permission(user)
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'OKK')
        return Manager.objects.all()
