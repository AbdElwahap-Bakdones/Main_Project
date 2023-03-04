from django.shortcuts import render
from django.db import models as MODELS, transaction
from Bank import models as MODELSBANK
# Create your views here.


def deposit(client, amount):
    try:
        with transaction.atomic():
            balance = MODELSBANK.Account.objects.select_for_update().get(
                client_name=client)
            print(f' bank account id {balance.pk}')
            balance.client_ammunt = balance.client_ammunt+amount
            balance.save()
            return balance.client_ammunt
    except Exception as e:
        return -1


def withdrawal(client, amount):
    try:
        with transaction.atomic():
            balance = MODELSBANK.Account.objects.select_for_update().get(
                client_name=client)
            if balance.client_ammunt < amount:
                return -1
            balance.client_ammunt = balance.client_ammunt-amount
            balance.save()
            return balance.client_ammunt
    except Exception as e:
        return -1
