
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from ..Relay import relays
import graphene
from notification.notification import Notification


class GetNotifications(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.NotificationConnection)

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_notification'):
                return QueryFields.rise_error(user)
            data = Notification.get(user)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('error in searchClubByName')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))
