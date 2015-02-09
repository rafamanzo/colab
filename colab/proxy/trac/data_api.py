from colab.proxy.utils.proxy_data_api import ProxyDataAPI
import time
from django.db import connections
from colab.proxy.trac.models import Attachment, Revision, Ticket, Wiki
from django.utils import timezone
from re import match


class TracDataAPI(ProxyDataAPI):

    def fetch_data(self):
        connection = connections['trac']
        cursor = connection.cursor()
        self.fetch_data_wiki(cursor)
        self.fetch_data_attachment(cursor)

    def fetch_data_attachment(self, cursor):
        attachment = Attachment()
        cursor.execute(''' SELECT * from attachment; ''')
        attachment_dict = self.dictfetchall(cursor)
        for line in attachment_dict:
            attachment.description = line['description']
            attachment.id = line['attach_id']
            attachment.filename = line['filemame']
            attachment.size = line['size']
            attachment.author = line['author']
            attachment.used_by = line['type']
            attachment.url = attachment.user_by + "/" + attachment.id \
                + "/" + attachment.filename
            local_time = line['time']/1000000
            attachment.created = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(local_time))
            if match("\.(\w+)$", attachment.filename):
                attachment.mimetype = attachment.filename.lower()
            attachment.save()

    def fetch_data_revision(self, cursor):
        revision = Revision()
        cursor.execute('''SELECT * FROM revision;''')
        revision_dict = self.dictfetchall(cursor)
        cursor.execute('''SELECT * FROM repository;''')
        repository_dict = self.dictfetchall(cursor)
        for line in revision_dict:
            revision.author = line['author']
            revision.rev = line['rev']
            revision.message = line['message']
            local_time = line['time']/1000000
            revision.created = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(local_time))
            revision.repository_name = repository_dict[line['value']]
    
    def fetch_data_ticket(self, cursor):
        ticket = Ticket()
        collaborators = []
        cursor.execute('''SELECT * FROM ticket;''')
        ticket_dict = self.dictfetchall(cursor)
        for line in ticket_dict:
            ticket.id = line['id']
            ticket.summary = line['summary']
            ticket.description = line['description']
            ticket.milestone = line['milestone']
            ticket.priority = line['priority']
            ticket.component = line['component']
            ticket.version = line['version']
            ticket.severity = line['severity']
            ticket.reporter = line['reporter']
            ticket.status = line['status']
            ticket.keywords = line['keywords']
            ticket.author = ticket.reporter
            local_time = line['time']/1000000
            ticket.created = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(local_time))
            ticket.modified = str(timezone.now())
            ticket.modified_by = ticket.author
            if line['report'] not in collaborators:
                   collaborators.append(line['report'])
            ticket.collaborators = collaborators
            

    def fetch_data_wiki(self, cursor):
        wiki = Wiki()
        cursor.execute('''SELECT * FROM wiki;''')
        wiki_dict = self.dictfetchall(cursor)
        collaborators = []

        for line in wiki_dict:
            wiki.update_user(line['author'])
            wiki.title = line['name']
            wiki.text = line['text']
            wiki.author = line['author']
            if line['author'] not in collaborators:
                    collaborators.append(line['author'])
            wiki.collaborators = collaborators
            local_time = line['time']/1000000
            wiki.created = time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.localtime(local_time))
            wiki.modified = str(timezone.now())
            wiki.save()

    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]
