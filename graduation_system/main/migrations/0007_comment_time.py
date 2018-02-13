# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-13 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date commented'),
            preserve_default=False,
        ),
    ]