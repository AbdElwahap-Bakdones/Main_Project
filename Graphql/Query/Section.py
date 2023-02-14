from core.models import Section
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene
from ..Auth.permission import checkPermission


class AllSectionByClub(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.SectionConnection, club_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not QueryFields.is_valide(info, user, 'core.add_club'):
            return QueryFields.rise_error(user)
        data = Section.objects.filter(club_id__manager_id__user_id=user,
                                      club_id__id=kwargs["club_id"], is_deleted=False)
        if not data.exists():
            QueryFields.NotFound(info=info)
        QueryFields.OK(info=info, data=data)


class GetSection(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.SectionConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        print(kwargs)
        return QueryFields.queryGet(Section, info, 'core.view_section', kwargs["id"])
