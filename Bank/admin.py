from django.contrib import admin
from .models import Account, ClientType, HistoryAccount, Operation
admin.site.register(Account)
admin.site.register(ClientType)
admin.site.register(HistoryAccount)
admin.site.register(Operation)
# Register your models here.
