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
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_section'):
            return QueryFields.rise_error(user)
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'OKK')
        return Section.objects.all()


class GetSection(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.SectionConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.view_section'):
            return QueryFields.rise_error(user)
        section = Section.objects.filter(id=kwargs["id"])
        if not section.exists():
            QueryFields.set_extra_data(
                user, status_code.HTTP_404_NOT_FOUND, 'not exists')
            return []
        QueryFields.set_extra_data(user, status_code.HTTP_200_OK, 'okk')
        return section
