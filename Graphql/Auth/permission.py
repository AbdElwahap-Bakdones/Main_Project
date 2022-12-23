from core.models import User


def checkPermission(permission: str, info: object):
    # print(dict(info.context.META))
    a = info.context.META["user"]
    if permission in a.get_all_permissions():
        return next
    raise Exception("You do not have permission to complete the process")
