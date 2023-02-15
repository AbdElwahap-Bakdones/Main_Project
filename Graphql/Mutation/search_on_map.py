from ..ModelsGraphQL import typeobject, inputtype
import graphene
from core import models, serializer
from ..Auth.permission import checkPermission
from .. import QueryStructure


class ChangeSearchOnMap(graphene.Mutation, QueryStructure.Attributes):
    data = graphene.Field(typeobject.PlayerObjectType)

    @classmethod
    def mutate(self, root, info, **kwargs):
        try:
            user = info.context.META["user"]
            if not checkPermission("core.change_player", user):
                return QueryStructure.NoPermission(self)
            player_obj = models.Player.objects.filter(user_id=user)
            if player_obj.get().available_on_map:
                player_obj.update(available_on_map=False)
            else:
                player_obj.update(available_on_map=True)
            return QueryStructure.OK(self, data=player_obj.get())
        except Exception as e:
            print('Error ChangeSearchOnMap !')
            print(str(e))
            return QueryStructure.InternalServerError(self, message=str(e))
