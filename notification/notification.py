from core import models


class notification():

    def add(sender: int, reciver: int, message: str, sender_kind: str, type: str) -> bool:
        if sender_kind == "user":
            note = models.Notification(
                sender_id=sender, reciver_id=reciver, sender_kind=sender_kind, type=type, content=message)
        if sender_kind == "team":
            note = models.Notification(
                sender_id=sender, team_id=reciver, sender_kind=sender_kind, type=type, content=message)
        else:
            return False
        note.save()
        return True

    def read(id: list[int]) -> bool:
        note = models.Notification.objects.filter(id__in=id, status=False)
        if not note.exists():
            return False
        note.update(status=True)
        return True

    def get(reciver_id: int) -> list[models.Notification.objects]:
        note = models.Notification.objects.filter(reciver_id=reciver_id)
        if not note.exists():
            return []
        return note
