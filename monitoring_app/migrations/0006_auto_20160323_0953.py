# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring_app', '0005_auto_20160323_0933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='machine',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='Address_machine',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='Name_machine',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='Password_machine',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='Username_machine',
            new_name='username',
        ),
    ]
