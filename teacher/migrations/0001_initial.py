# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 06:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=10)),
                ('work_place', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=25)),
                ('research_area', models.CharField(max_length=30)),
                ('recruit_number', models.IntegerField()),
                ('url', models.URLField()),
            ],
        ),
    ]