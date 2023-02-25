from django.db import models


class ClientType(models.Model):
    name = models.CharField(max_length=50)


class Account(models.Model):
    client_name = models.CharField(unique=True, max_length=150)
    client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE)
    client_ammunt = models.FloatField(default=0)


class Operation(models.Model):
    name = models.CharField(max_length=50)


class HistoryAccount(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    ammunt = models.FloatField()
