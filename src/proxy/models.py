# -*- coding: utf-8 -*-

from django.db import models

from accounts.models import User
from hitcount.models import HitCountModelMixin


class Attachment(models.Model, HitCountModelMixin):
    url = models.TextField(primary_key=True)
    type = models.TextField()
    filename = models.TextField()
    author = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(blank=True)
    mimetype = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'attachment_view'

    def get_absolute_url(self):
        return u'/raw-attachment/{}'.format(self.url)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None


class Revision(models.Model, HitCountModelMixin):
    key = models.TextField(blank=True, primary_key=True)
    rev = models.TextField(blank=True)
    author = models.TextField(blank=True)
    message = models.TextField(blank=True)
    repository_name = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'revision_view'

    def get_absolute_url(self):
        return u'/changeset/{}/{}'.format(self.rev, self.repository_name)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None

class Ticket(models.Model, HitCountModelMixin):
    id = models.IntegerField(primary_key=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    milestone = models.TextField(blank=True)
    priority = models.TextField(blank=True)
    component = models.TextField(blank=True)
    version = models.TextField(blank=True)
    severity = models.TextField(blank=True)
    reporter = models.TextField(blank=True)
    author = models.TextField(blank=True)
    status = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    collaborators = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_view'

    def get_absolute_url(self):
        return u'/ticket/{}'.format(self.id)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None


class Wiki(models.Model, HitCountModelMixin):
    name = models.TextField(primary_key=True)
    wiki_text = models.TextField(blank=True)
    author = models.TextField(blank=True)
    collaborators = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_view'

    def get_absolute_url(self):
        return u'/wiki/{}'.format(self.name)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None
