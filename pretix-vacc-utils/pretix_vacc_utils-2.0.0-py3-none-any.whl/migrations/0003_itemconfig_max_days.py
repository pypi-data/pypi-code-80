# Generated by Django 3.0.11 on 2021-03-26 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pretix_vacc_autosched", "0002_auto_20210310_1210"),
    ]

    operations = [
        migrations.AddField(
            model_name="itemconfig",
            name="max_days",
            field=models.IntegerField(null=True),
        ),
    ]
