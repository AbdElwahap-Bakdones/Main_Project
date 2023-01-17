from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from core import models
from ..Relay import relays
import graphene


class ClubSubManagerd(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.SubManagerConnection, club=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        sub_manager = models.SubManager.objects.filter(club_id=kwargs['club'])
        return QueryFields.OK(info=info, data=sub_manager)


class GetSection(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.SectionConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.OK(info=info)
