# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-04-26 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_active',
            field=models.BigIntegerField(default=False, verbose_name='邮箱验证状态'),
        ),
    ]
