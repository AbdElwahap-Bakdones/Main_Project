from core.models import Section, Club, Manager, SubManager
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
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.add_club'):
                return QueryFields.rise_error(user)
            club_obj = Club.objects.filter(
                id=kwargs['club_id'], manager_id__user_id=user, is_deleted=False)
            if not club_obj.exists():
                return QueryFields.BadRequest(info=info)
            data = Section.objects.filter(
                club_id__in=club_obj.values_list('pk', flat=True), is_deleted=False)
            if not data.exists():
                return QueryFields.NotFound(info=info)
            return QueryFields.OK(info=info, data=data)
        except Exception as e:
            print('Error in AllSectionByClub')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))


class GetSection(ObjectType, QueryFields):
    data = relay.ConnectionField(
        relays.SectionConnection, id=graphene.ID(required=True))

    def resolve_data(root, info, **kwargs):
        try:
            user = info.context.META['user']
            if not QueryFields.is_valide(info, user, 'core.add_section'):
                return QueryFields.rise_error(user)
            section_obj = Section.objects.filter(club_id__manager_id__user_id=user,
                                                 pk=kwargs['id'], is_deleted=False, club_id__is_deleted=False)
            if section_obj.exists():
                return QueryFields.OK(info, data=section_obj)
            return QueryFields.NotFound(info)
        except Exception as e:
            print('error in GetSection')
            print(e)
            return QueryFields.ServerError(info, msg=str(e))


# class GetSectionByClub(ObjectType, QueryFields):
#     data = relay.ConnectionField(
#         relays.SectionConnection, club_id=graphene.ID(required=True))

#     def resolve_data(root, info, **kwargs):
#         try:
#             user = info.context.META['user']
#             if not QueryFields.is_valide(info, user, 'core.add_section'):
#                 return QueryFields.rise_error(user)
#             section_obj = Section.objects.filter(
#                 club_id__manager_id__user_id=user, club_id__id=kwargs['club_id'], is_deleted=False, club_id__is_deleted=False)
#             if section_obj.exists():
#                 return QueryFields.OK(info, data=section_obj)
#             return QueryFields.NotFound(info)
#         except Exception as e:
#             print('error in GetSection')
#             print(e)
#             return QueryFields.ServerError(info, msg=str(e))
