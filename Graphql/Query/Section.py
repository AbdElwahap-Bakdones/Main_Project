from core.models import Section
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene


class AllSection(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.SectionConnection)

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryAll(Section, info, 'core.view_section')


class GetSection(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.SectionConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryGet(Section, info, 'core.view_section', kwargs["id"])
