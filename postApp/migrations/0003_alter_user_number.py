# Generated by Django 4.1.2 on 2022-10-22 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("postApp", "0002_rename_emial_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="number",
            field=models.IntegerField(max_length=25),
        ),
    ]