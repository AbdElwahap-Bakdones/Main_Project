# Generated by Django 4.1.2 on 2022-10-22 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("postApp", "0003_alter_user_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="number",
        ),
    ]