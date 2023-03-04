from ..ModelsGraphQL import typeobject, inputtype
import graphene
from ..Auth.permission import checkPermission
from .. import QueryStructure
from notification.notification import Notification


class ReadNotification(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Boolean()

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_notification", user):
                return QueryStructure.NoPermission(self)
            data = Notification.read(user)
            return QueryStructure.OK(instanse=self, data=data)
        except Exception as e:
            print('Error in ReadNotification')
            print(e)
            return False
