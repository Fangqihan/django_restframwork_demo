# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-13 02:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('type', models.IntegerField(choices=[(1, '普通用户'), (2, '管理用户')], default=1)),
                ('email', models.EmailField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo'),
        ),
    ]