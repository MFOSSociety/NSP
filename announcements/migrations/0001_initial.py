# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-18 12:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation_date')),
                ('site_wide', models.BooleanField(default=False, verbose_name='site wide')),
                ('members_only', models.BooleanField(default=False, verbose_name='members only')),
                ('dismissal_type', models.IntegerField(choices=[(1, 'No Dismissals Allowed'), (2, 'Session Only Dismissal'), (3, 'Permanent Dismissal Allowed')], default=2)),
                ('publish_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publish_start')),
                ('publish_end', models.DateTimeField(blank=True, null=True, verbose_name='publish_end')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name': 'announcement',
                'verbose_name_plural': 'announcements',
            },
        ),
        migrations.CreateModel(
            name='Dismissal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dismissed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dismissals', to='announcements.Announcement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcement_dismissals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]