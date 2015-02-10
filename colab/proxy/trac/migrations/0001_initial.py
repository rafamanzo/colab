# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import hitcounter.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('url', models.TextField(serialize=False, primary_key=True)),
                ('attach_id', models.TextField()),
                ('used_by', models.TextField()),
                ('filename', models.TextField()),
                ('author', models.TextField(blank=True)),
                ('title', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('modified', models.DateTimeField(blank=True)),
                ('mimetype', models.TextField(blank=True)),
                ('size', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachment',
            },
            bases=(models.Model, hitcounter.models.HitCounterModelMixin),
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('key', models.TextField(serialize=False, primary_key=True, blank=True)),
                ('rev', models.TextField(blank=True)),
                ('author', models.TextField(blank=True)),
                ('message', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('repository_name', models.TextField(blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'trac_revision',
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachment',
            },
            bases=(models.Model, hitcounter.models.HitCounterModelMixin),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('summary', models.TextField(blank=True)),
                ('description_ticket', models.TextField(blank=True)),
                ('milestone', models.TextField(blank=True)),
                ('priority', models.TextField(blank=True)),
                ('component', models.TextField(blank=True)),
                ('version', models.TextField(blank=True)),
                ('severity', models.TextField(blank=True)),
                ('reporter', models.TextField(blank=True)),
                ('author', models.TextField(blank=True)),
                ('status', models.TextField(blank=True)),
                ('tag', models.TextField(blank=True)),
                ('keywords', models.TextField(blank=True)),
                ('collaborators', models.TextField(blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('modified_by', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachment',
            },
            bases=(models.Model, hitcounter.models.HitCounterModelMixin),
        ),
        migrations.CreateModel(
            name='TicketCollabCount',
            fields=[
                ('author', models.TextField(serialize=False, primary_key=True)),
                ('count', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wiki',
            fields=[
                ('title', models.TextField(serialize=False, primary_key=True)),
                ('wiki_text', models.TextField(blank=True)),
                ('author', models.TextField(blank=True)),
                ('collaborators', models.TextField(blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachment',
            },
            bases=(models.Model, hitcounter.models.HitCounterModelMixin),
        ),
        migrations.CreateModel(
            name='WikiCollabCount',
            fields=[
                ('author', models.TextField(serialize=False, primary_key=True)),
                ('count', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachment',
            },
            bases=(models.Model,),
        ),
    ]
