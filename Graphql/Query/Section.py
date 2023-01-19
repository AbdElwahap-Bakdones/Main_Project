from core import models
from graphene import ObjectType, relay
from Graphql.QueryStructure import QueryFields
from rest_framework import status as status_code
from ..Relay import relays
import graphene

# manager example :in selector add stadium
class AllSection(ObjectType, QueryFields):
    data = relay.ConnectionField(relays.SectionConnection,club_id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not models.Manager.objects.filter(user_id=user).exists():
            return QueryFields.BadRequest(info=info)
        data = models.Section.objects.filter(club_id__id=kwargs["club_id"],club_id__user_id=user, is_deleted=False)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)

# manager search on section by name
class GetSection(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.SectionConnection,club_id=graphene.ID(required=True),section_name=graphene.String(required=True))

    def resolve_data(root, info, **kwargs):
        user = info.context.META['user']
        if not models.Manager.objects.filter(user_id=user).exists():
            return QueryFields.BadRequest(info=info)
        data = models.Section.objects.filter(pk=kwargs["section_id"],club_id__id=kwargs["club_id"],club_id__user_id=user, is_deleted=False)
        if not data.exists():
            return QueryFields.NotFound(info=info)
        return QueryFields.OK(info=info, data=data)