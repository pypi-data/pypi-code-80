# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-24 00:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # noqa
                ('source_display_name', models.CharField(max_length=150)),
                ('action', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('obj', models.IntegerField()),
                ('url', models.URLField()),
                ('is_read', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('short_description', models.CharField(max_length=100)),
                ('recipent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),  # noqa
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # noqa
            ],
        ),
    ]
