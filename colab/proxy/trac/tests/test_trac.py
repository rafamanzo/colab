"""
Test Trac class.
Objective: Test parameters and behavior.
"""
from colab.accounts.models import User
from colab.proxy.trac.models import Attachment, Revision, Ticket, Wiki
from django.test import TestCase


class AttachmentTest(TestCase):

    def setUp(self):
        self.attachment = self.create_attachment()

    def tearDown(self):
        pass

    def create_attachment(self):
        attachment = Attachment()
        attachment.type = 'attachment'
        attachment.icon_name = 'file'
        attachment.url = 'example.com'
        attachment.attach_id = 'attach_id'
        attachment.used_by = 'used_by'
        attachment.filename = 'filename'
        attachment.author = 'author'
        attachment.title = 'title'
        attachment.description = 'description'
        attachment.modified = '1994-11-05T08:15:30-05:00'
        attachment.mimetype = 'mimetype'
        attachment.size = 20
        attachment.save()

        return attachment

    def test_validade_filepath(self):
        file_path = '/mnt/trac/attachments/used_by/attach_id/filename'
        self.assertEqual(file_path, self.attachment.filepath)

    def test_validade_absolute_url(self):
        absolute_url = u'/raw-attachment/example.com'
        self.assertEqual(absolute_url, self.attachment.get_absolute_url())

    def test_validade_author(self):
        author = 'author'
        self.user = create_user()
        self.assertEqual(author, str(self.attachment.get_author()))

    def test_invalidade_author(self):
        self.assertEqual(None, self.attachment.get_author())


class RevisionTest(TestCase):
    def setUp(self):
        self.revision = self.create_revision()

    def create_revision(self):
        revision = Revision()
        revision.update_field = 'created'
        revision.icon_name = 'align-right'
        revision.rev = 'rev'
        revision.author = 'author'
        revision.message = 'message'
        revision.description = 'description'
        revision.repository_name = 'repository'
        revision.created = '1994-11-05T08:15:30-05:00'
        revision.modified = '1994-11-05T08:15:30-05:00'
        revision.save()

        return revision

    def test_title(self):
        title = 'repository [rev]'
        self.assertEqual(title, self.revision.title)

    def test_get_absolute_url(self):
        absolute_url = '/changeset/rev/repository'
        self.assertEqual(absolute_url, self.revision.get_absolute_url())

    def test_get_author(self):
        author = 'author'
        self.user = create_user()
        self.assertEqual(author, str(self.revision.get_author()))

    def test_invalid_get_author(self):
        self.assertEqual(None, self.revision.get_author())


class TicketTest(TestCase):
    def setUp(self):
        self.ticket = self.create_ticket()

    def create_ticket(self):
        ticket = Ticket()
        ticket.icon_name = 'tag'
        ticket.type = 'ticket'
        ticket.id = 20
        ticket.summary = 'summary'
        ticket.description_ticket = 'description'
        ticket.milestone = 'milestone'
        ticket.priority = 'priority'
        ticket.component = 'component'
        ticket.version = 'version'
        ticket.severity = 'severity'
        ticket.reporter = 'reporter'
        ticket.author = 'author'
        ticket.status = 'status'
        ticket.tag = 'tag'
        ticket.keywords = 'keywords'
        ticket.collaborators = 'collaborators'
        ticket.created = '1994-11-05T08:15:30-05:00'
        ticket.modified = '1994-11-05T08:15:30-05:00'
        ticket.modified_by = 'author'
        ticket.save()

        return ticket

    def test_title(self):
        title = '#20 - summary'
        self.assertEqual(title, self.ticket.title)

    def test_description(self):
        description1 = u'description\nmilestone\ncomponent\nseverity'
        description2 = '\nreporter\nkeywords\ncollaborators'
        description_test = description1 + description2
        self.assertEqual(description_test, self.ticket.description)

    def test_get_absolute_url(self):
        absolute_url = '/ticket/20'
        self.assertEqual(absolute_url, self.ticket.get_absolute_url())

    def test_get_author(self):
        author = 'author'
        self.user = create_user()
        self.assertEqual(author, str(self.ticket.get_author()))

    def test_invalid_get_author(self):
        author = None
        self.assertEqual(author, self.ticket.get_author())

    def test_get_modified_by(self):
        self.user = create_user()
        get_modified_by = str(self.ticket.get_modified_by())
        self.assertEqual(self.ticket.modified_by, get_modified_by)

    def test_invalid_get_modified_by(self):
        get_modified_by = self.ticket.get_modified_by()
        self.assertEqual(None, get_modified_by)


class WikiTest(TestCase):
    def setUp(self):
        self.wiki = self.create_wiki()

    def create_wiki(self):
        wiki = Wiki()
        wiki.type = "wiki"
        wiki.icon_name = "book"
        wiki.title = 'title'
        wiki.wiki_text = 'wiki_text'
        wiki.author = 'author'
        wiki.collaborators = 'collaborators'
        wiki.created = '1994-11-05T08:15:30-05:00'
        wiki.modified = '1994-11-05T08:15:30-05:00'
        from django.conf import settings
        print settings.INSTALLED_APPS
        wiki.save()

        return wiki

    def test_description(self):
        description_test = u'wiki_text\ncollaborators'
        self.assertEqual(description_test, self.wiki.description)

    def test_get_absolute_url(self):
        absolute_url = u'/wiki/title'
        self.assertEqual(absolute_url, self.wiki.get_absolute_url())

    def test_get_author(self):
        author = 'author'
        self.user = create_user()
        self.assertEqual(author, str(self.wiki.get_author()))

    def test_invalid_get_author(self):
        author = None
        self.assertEqual(author, self.wiki.get_author())

    def test_get_modified_by(self):
        self.user = create_user()
        get_modified_by = str(self.wiki.get_modified_by())
        modified_by = "author"
        self.assertEqual(modified_by, get_modified_by)

    def test_invalid_get_modified_by(self):
        get_modified_by = self.wiki.get_modified_by()
        self.assertEqual(None, get_modified_by)


def create_user():
    user = User()
    user.username = "author"
    user.first_name = "FisrtName"
    user.last_name = "LastName"
    user.modified_by = "author"
    user.save()

    return user
