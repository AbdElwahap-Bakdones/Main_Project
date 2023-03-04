
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from ..Relay import relays
import graphene
from notification.notification import Notification


class GetNotifications(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.NotificationConnection)
    count_notif = graphene.Int()

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.view_notification'):
                return QueryFields.rise_error(user)
            data = Notification.get(user)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('error in GetNotifications.resolve_data')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))

    def resolve_count_notif(root, info):
        try:
            user = info.context.META['user']
            data = Notification.get_count(user)
            return data
        except Exception as e:
            print('error in resolve_count_notif.resolve_count')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))
