# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-24 21:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynoquiz', '0010_auto_20160623_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.IntegerField(default=0)),
                ('incorrect', models.IntegerField(default=0)),
                ('quiz_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='dynoquiz.QuizUser')),
            ],
        ),
    ]
