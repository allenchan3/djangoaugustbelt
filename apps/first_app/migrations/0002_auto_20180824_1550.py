# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-24 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itemlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_user_added', to='first_app.User')),
                ('item_favorited_by_users', models.ManyToManyField(related_name='user_favorite_items', to='first_app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='movielist',
            name='movie_added_by',
        ),
        migrations.RemoveField(
            model_name='movielist',
            name='movie_favorited_by_users',
        ),
        migrations.DeleteModel(
            name='Movielist',
        ),
    ]
