# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 08:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swacch', '0004_sessiontoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='user_images')),
                ('image_url', models.CharField(max_length=255)),
                ('caption', models.CharField(max_length=240)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swacch.User')),
            ],
        ),
    ]
