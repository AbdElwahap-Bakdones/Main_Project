from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from core import models
from ..Relay import relays
import graphene


class ClubSubManagerd(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.SubManagerConnection, club=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info=info, user=user, operation='core.view_submanager'):
            return QueryFields.rise_error(user=user)
        if not models.Club.objects.filter(manager_id__user_id=user.pk, pk=kwargs['club']).exists():
            return QueryFields.BadRequest(info=info)

        sub_manager = models.SubManager.objects.filter(club_id=kwargs['club'])
        return QueryFields.OK(info=info, data=sub_manager)
