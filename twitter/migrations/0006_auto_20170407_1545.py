# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0005_auto_20170407_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(upload_to=''),
        ),
    ]
