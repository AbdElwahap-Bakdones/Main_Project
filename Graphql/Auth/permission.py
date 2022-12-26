from core.models import User


def checkPermission(permission: str, user: object):
    # print(dict(info.context.META))
    if permission in user.get_all_permissions():
        return True
    return False
