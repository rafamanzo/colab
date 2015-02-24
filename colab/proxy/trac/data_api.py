from datetime import datetime
from re import match
from time import mktime
import time
import pytz

from django.db import connections
from django.utils import timezone
from django.utils.timezone import get_current_timezone_name

from colab.proxy.trac.models import Attachment, Revision, Ticket, Wiki
from colab.proxy.utils.proxy_data_api import ProxyDataAPI

class TracDataAPI(ProxyDataAPI):

    def fetch_data(self):
        connection = connections['trac']
        cursor = connection.cursor()
        self.fetch_data_wiki(cursor)
        self.fetch_data_attachment(cursor)
        self.fetch_data_ticket(cursor)
        self.fetch_data_revision(cursor)

    def fetch_data_attachment(self, empty_cursor):
        attachment = Attachment()
        cursor = self.attachment_cursor(empty_cursor)
        attachment_dict = self.dictfetchall(cursor)
        time_zone = pytz.timezone(get_current_timezone_name())	
        for line in attachment_dict:
            attachment.description = line['description']
            attachment.id = attachment.attach_id 
            attachment.filename = line['filename']
            attachment.title = attachment.filename
            attachment.size = line['size']
            attachment.author = line['author']
            attachment.used_by = line['type']
            attachment.url = attachment.used_by + "/" + attachment.id \
                + "/" + attachment.filename
            local_time = line['time']/1000000
            naive_date_time = datetime.fromtimestamp(mktime(time.localtime(local_time)))
            attachment.created = time_zone.localize(naive_date_time, is_dst=None).astimezone(pytz.utc)          

            attachment.modified = time.strftime('%Y-%m-%d %H:%M:%S',
                                                time.localtime(local_time))
            if match("\.(\w+)$", attachment.filename):
                attachment.mimetype = attachment.filename.lower()
            attachment.save()

    def fetch_data_revision(self, empty_cursor):
        revision = Revision()
        cursor = self.revision_cursor(empty_cursor)
        revision_dict = self.dictfetchall(cursor)
        cursor = self.repository_cursor(empty_cursor)
        repository_dict = self.dictfetchall(cursor)
        time_zone = pytz.timezone(get_current_timezone_name())	
        for line in revision_dict:
            revision.author = line['author']
            revision.rev = line['rev']
            revision.message = line['message']
            revision.description = revision.message
            local_time = line['time']/1000000
            naive_date_time = datetime.fromtimestamp(mktime(time.localtime(local_time)))
            revision.created = time_zone.localize(naive_date_time, is_dst=None).astimezone(pytz.utc)
            revision.repository_name = repository_dict[line['repos']]

    def fetch_data_ticket(self, empty_cursor):
        ticket = Ticket()
        collaborators = []
        cursor = self.ticket_cursor(empty_cursor)
        ticket_dict = self.dictfetchall(cursor)
        time_zone = pytz.timezone(get_current_timezone_name())	
        for line in ticket_dict:
            ticket.id = line['id']
            ticket.summary = line['summary']
            ticket.description_ticket = line['description']
            ticket.milestone = line['milestone']
            ticket.priority = line['priority']
            ticket.component = line['component']
            ticket.version = line['version']
            ticket.severity = line['severity']
            ticket.reporter = line['reporter']
            ticket.status = line['status']
            ticket.tag = ticket.status
            ticket.keywords = line['keywords']
            ticket.author = ticket.reporter
            local_time = line['time']/1000000
            naive_date_time = datetime.fromtimestamp(mktime(time.localtime(local_time)))
            ticket.created = time_zone.localize(naive_date_time, is_dst=None).astimezone(pytz.utc)
            ticket.modified = str(timezone.now())
            ticket.modified_by = ticket.author
            if line['reporter'] not in collaborators:
                collaborators.append(line['reporter'])
            ticket.collaborators = collaborators

    def fetch_data_wiki(self, empty_cursor):
        wiki = Wiki()
        cursor = self.wiki_cursor(empty_cursor)
        wiki_dict = self.dictfetchall(cursor)
        collaborators = []
        time_zone = pytz.timezone(get_current_timezone_name())	
        for line in wiki_dict:
            wiki.update_user(line['author'])
            wiki.title = line['name']
            wiki.text = line['text']
            wiki.author = line['author']
            if line['author'] not in collaborators:
                    collaborators.append(line['author'])
            wiki.collaborators = collaborators
            local_time = line['time']/1000000
            naive_date_time = datetime.fromtimestamp(mktime(time.localtime(local_time)))
            wiki.created = time_zone.localize(naive_date_time, is_dst=None).astimezone(pytz.utc)
            wiki.modified = str(timezone.now())
            wiki.save()

    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]

    def wiki_cursor(self, cursor):
        cursor.execute('''SELECT * FROM wiki;''')
        return cursor

    def attachment_cursor(self, cursor):
        cursor.execute('''SELECT * FROM attachment;''')
        return cursor

    def ticket_cursor(self, cursor):
        cursor.execute('''SELECT * FROM ticket;''')
        return cursor

    def revision_cursor(self, cursor):
        cursor.execute('''SELECT * FROM revision;''')
        return cursor

    def repository_cursor(self, cursor):
        cursor.execute('''SELECT * FROM repository;''')
        return cursor
