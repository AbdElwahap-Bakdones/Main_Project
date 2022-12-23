from django.contrib import admin
from django.apps import apps
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# admin.site.register(User)
app = apps.get_app_config('core')
for model_name, model in app.models.items():
    if model == User:
        continue
    admin.site.register(model)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

# Register your models here.
