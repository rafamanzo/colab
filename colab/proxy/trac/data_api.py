from re import match
from time import mktime
import datetime

from django.db import connections

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
        for line in attachment_dict:
            attachment.description = line['description']
            attachment.id = line['id']
            attachment.filename = line['filename']
            attachment.title = attachment.filename
            attachment.size = line['size']
            attachment.author = line['author']
            attachment.used_by = line['type']
            attachment.ipnr = line['ipnr']
            attachment.url = attachment.used_by + "/" + attachment.id \
                + "/" + attachment.filename
            attachment.created = self.get_attachment_created(cursor, line['id'])
            if match("\.(\w+)$", attachment.filename):
                attachment.mimetype = attachment.filename.lower()
            attachment.save()

    def fetch_data_revision(self, empty_cursor):
        revision = Revision()
        cursor = self.revision_cursor(empty_cursor)
        revision_dict = self.dictfetchall(cursor)
        cursor = self.repository_cursor(empty_cursor)
        repository_dict = self.dictfetchall(cursor)
        for line in revision_dict:
            revision.author = line['author']
            revision.rev = line['rev']
            revision.message = line['message']
            revision.description = revision.message
            revision.created = self.get_revision_created(cursor, line['rev'])
            revision.repository_name = repository_dict[line['repos']]

    def fetch_data_ticket(self, empty_cursor):
        ticket = Ticket()
        collaborators = []
        cursor = self.ticket_cursor(empty_cursor)
        ticket_dict = self.dictfetchall(cursor)
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
            ticket.owner = line['owner']
            ticket.resolution = line['resolution']
            ticket.author = ticket.reporter
            ticket.created = self.get_ticket_created(cursor, line['id'])
            ticket.modified = self.get_ticket_modified(cursor, line['id'])
            ticket.modified_by = ticket.author
            if line['reporter'] not in collaborators:
                collaborators.append(line['reporter'])
            ticket.collaborators = collaborators

    def fetch_data_wiki(self, empty_cursor):
        wiki = Wiki()
        cursor = self.wiki_cursor(empty_cursor)
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
            wiki.created =self.get_wiki_created(cursor, line['name'])
            wiki.modified = self.get_wiki_modified(cursor, line['name'])

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

    def get_wiki_modified(self, cursor, wiki_name):
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + (MAX(wiki.time)/1000000) * INTERVAL '1s', name from wiki where(name=\'"""+ wiki_name + """\') group by name; """)
        matriz_data_wiki  = cursor.fetchall()
        modified_data = matriz_data_wiki[0][0]
        return modified_data

    def get_wiki_created(self, cursor, wiki_name):
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(wiki.time)/1000000) * INTERVAL '1s', name from wiki where(name=\'"""+ wiki_name + """\') group by name; """)
        matrix_data_wiki  = cursor.fetchall()
        modified_data = matrix_data_wiki[0][0]
        return modified_data

    def get_attachment_created(self, cursor, attachment_id):
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(attachment.time)/1000000) * INTERVAL '1s', id from attachment where(id=\'"""+ attachment_id + """\') group by id; """)
        matriz_data_attachment = cursor.fetchall()
        modified_data = matriz_data_attachment[0][0]
        return modified_data

    def get_revision_created(self, cursor, revision):
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(revision.time)/1000000) * INTERVAL '1s', rev from revision where(rev=\'"""+ revision + """\') group by rev; """)
        matriz_data_revision = cursor.fetchall()
        modified_data = matriz_data_revision[0][0]
        return modified_data

    def get_ticket_created(self, cursor, ticket_id):
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(ticket.time)/1000000) * INTERVAL '1s', id from ticket where(id="""+ str(ticket_id) + """) group by id; """)
        matriz_data_ticket = cursor.fetchall()
        modified_data = matriz_data_ticket[0][0]
        return modified_data

    def get_ticket_modified(self, cursor, ticket_id):
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + (MAX(ticket.time)/1000000) * INTERVAL '1s', id from ticket where(id="""+ str(ticket_id) + """) group by id; """)
        matriz_data_ticket = cursor.fetchall()
        modified_data = matriz_data_ticket[0][0]
        return modified_data
