from django.contrib import admin
from django.apps import apps
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# admin.site.register(User)
app = apps.get_app_config('core')
for model_name, model in app.models.items():
    if model == models.User or model == models.Friend:
        continue
    admin.site.register(model)


@admin.register(models.Friend)
class FrindAdmin(admin.ModelAdmin):
    list_display = ['player1', 'player2', 'state', 'sender']


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    pass

# Register your models here.
