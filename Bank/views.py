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


def get_balance(client_name: str, client_type: str) -> float:
    try:
        if client_type == 'player':
            name = ""+str(client_name)+"_"+str(1)
        if client_type == 'club':
            name = ""+str(client_name)+"_"+str(2)

        balance = MODELSBANK.Account.objects.filter(client_ammunt=name)
        if balance.exists():
            return balance.first().client_ammunt
        return -1
    except Exception as e:
        print('Error in Bank get_balance !')
        print(e)
        return -1


def create_account(client_name: str, client_type: str) -> bool:
    try:
        if client_type == 'player':
            name = ""+str(client_name)+"_"+str(1)
            account = MODELSBANK.Account(client_name=name,
                                         client_type=MODELSBANK.ClientType.objects.get(pk=1))
            account.save()
            return True
        if client_type == 'club':
            name = ""+str(client_name)+"_"+str(2)
            account = MODELSBANK.Account(client_name=name,
                                         client_type=MODELSBANK.ClientType.objects.get(pk=2))
            account.save()
            return True
        return False
    except Exception as e:
        print('Error in Bank create_account !')
        print(e)
        return False
