from core import models, serializer


class Notification():
    def has_notif(user: models.User) -> int:
        try:
            data = models.Notification.objects.filter(
                reciver_id=user, is_read=False)
            print(data.values())
            if data.exists():
                return True
            return False
        except Exception as e:
            print('Error in Notification.has_notif')
            print(e)
            return False

    def get_count(user: models.User) -> int:
        try:
            data = models.Notification.objects.filter(
                reciver_id=user, is_read=False).count()
            return data
        except Exception as e:
            print('Error in Notification.get_count')
            print(e)
            return False

    def add(sender: int, reciver: int, message: str, sender_kind: str, type: str) -> bool:
        if sender_kind == "user":

            data = {'sender_id': sender, 'reciver_id': reciver,
                    'sender_kind': sender_kind, 'type': type, 'content': message}
            seria = serializer.NotificationSerializer(data=data)
            if seria.is_valid():
                seria.save()
                return True
            else:
                print('Error in Notification.add!')
                print(seria.errors)
                return False
        if sender_kind == "team":
            data = {'sender_id': sender, 'reciver_id': reciver,
                    'sender_kind': sender_kind, 'type': type, 'content': message}
            seria = serializer.NotificationSerializer(data=data)
            if seria.is_valid():
                seria.save()
                return True
            else:
                print('Error in Notification.add!')
                print(seria.errors)
                return False
        else:
            return False

    def read(user: models.User) -> bool:
        try:
            models.Notification.objects.filter(
                reciver_id=user, is_read=False).update(is_read=True)
            return True
        except Exception as e:
            print('Error in Notification.read')
            print(e)
            return False

    def get(user: models.User) -> list[models.Notification.objects]:
        try:
            note = models.Notification.objects.filter(
                reciver_id=user).order_by('-date')
            return note
        except Exception as e:
            print('Error in Notification.get')
            print(e)
            return False
