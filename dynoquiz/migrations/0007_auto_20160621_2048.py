# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-21 20:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dynoquiz', '0006_question_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='users',
            field=models.ManyToManyField(related_name='quizzes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_quizzes', to=settings.AUTH_USER_MODEL),
        ),
    ]
