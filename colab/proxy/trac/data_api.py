# -*- coding: utf-8 -*-
from re import match

from django.db import connections

from colab.proxy.trac.models import Attachment, Revision, Ticket, Wiki
from colab.proxy.utils.proxy_data_api import ProxyDataAPI


class TracDataAPI(ProxyDataAPI):

    def fetch_data(self):
        """ This is the pricipal method whose function is just make the call the
        other methods.

        """
        connection = connections['trac']
        cursor = connection.cursor()
        self.fetch_data_wiki(cursor)
        self.fetch_data_attachment(cursor)
        self.fetch_data_ticket(cursor)
        self.fetch_data_revision(cursor)

    def fetch_data_attachment(self, empty_cursor):
        """ This method is responsible for seeking the attachment data in
        trac database and transfer them to the colab database.

        :param empty_cursor: A cursor coming from connectinos, it is necessary
            import the connections library from django.db, with it we can run
            sql commands.

        :returns: Return is an attachment object with your saved data
            in the colab database.

        """
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
            attachment.created = self.get_attachment_created(cursor,
                                                             line['id'])
            if match("\.(\w+)$", attachment.filename):
                attachment.mimetype = attachment.filename.lower()
            attachment.save()

    def fetch_data_revision(self, empty_cursor):
        """ This method is responsible for seeking the revision data in
        trac database and transfer them to the colab database.

        :param empty_cursor: A cursor coming from connectinos, it is necessary
            import the connections library from django.db, with it we can run
            sql commands.

        :returns: Return is an revision object with your saved data
            in the colab database.

        """
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
            revision.repository_name = line['repos']
            revision.save()

    def fetch_data_ticket(self, empty_cursor):
        """ This method is responsible for seeking the ticket data in
        trac database and transfer them to the colab database.

        :param empty_cursor: A cursor coming from connectinos, it is necessary
            import the connections library from django.db, with it we can run
            sql commands.

        :returns: Return is an ticker object with your saved data
            in the colab database.

        """
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
            if line['keywords']:
                ticket.keywords = line['keywords']
            if line['owner']:
                ticket.owner = line['owner']
            else:
                ticket.owner = 'Anonymous'
            if line['resolution']:
                ticket.resolution = line['resolution']
            else:
                ticket.resolution = 'no resolution'
            ticket.author = ticket.reporter
            ticket.created = self.get_ticket_created(cursor, line['id'])
            ticket.modified = self.get_ticket_modified(cursor, line['id'])
            if line['reporter'] not in collaborators:
                collaborators.append(line['reporter'])
            ticket.collaborators = collaborators
            ticket.update_user(ticket.author)
            ticket.save()

    def fetch_data_wiki(self, empty_cursor):
        """ This method is responsible for seeking the wiki data in
        trac database and transfer them to the colab database.

        :param empty_cursor: A cursor coming from connectinos, it is necessary
            import the connections library from django.db, with it we can run
            sql commands.

        :returns: Return is an wiki object with your saved data
            in the colab database.

        """
        wiki = Wiki()
        cursor = self.wiki_cursor(empty_cursor)
        wiki_dict = self.dictfetchall(cursor)
        collaborators = []
        for line in wiki_dict:
            wiki.update_user(line['author'])
            wiki.title = line['name']
            wiki.wiki_text = line['text']
            wiki.author = line['author']
            if line['author'] not in collaborators:
                    collaborators.append(line['author'])
            wiki.collaborators = collaborators
            wiki.created = self.get_wiki_created(cursor, line['name'])
            wiki.modified = self.get_wiki_modified(cursor, line['name'])

            wiki.save()

    def dictfetchall(self, cursor):
        """ This method is responsible for taking the cursor content
        and turn it into a dictionary.

        The cursor returns an array of tuples, With this method it will return
        a list of dictionaries..

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :returns: Return are cursor.fetchall() in the format of dictionary

        """
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]

    def wiki_cursor(self, cursor):
        """ This is the method in charge of getting the wiki table data and
        put them in the cursor.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :returns: The return is the result of the desired query

        """
        cursor.execute('''SELECT * FROM wiki;''')
        return cursor

    def attachment_cursor(self, cursor):
        """ This is the method in charge of getting the attachment table data and
        put them in the cursor.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :returns: The return is the result of the desired query

        """
        cursor.execute('''SELECT * FROM attachment;''')
        return cursor

    def ticket_cursor(self, cursor):
        """ This is the method in charge of getting the ticket table data and
        put them in the cursor.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :returns: The return is the result of the desired query

        """
        cursor.execute('''SELECT * FROM ticket;''')
        return cursor

    def revision_cursor(self, cursor):
        """ This is the method in charge of getting the revision table data and
        put them in the cursor.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :returns: The return is the result of the desired query

        """
        cursor.execute('''SELECT * FROM revision;''')
        return cursor

    def repository_cursor(self, cursor):
        """ This is the method in charge of getting the repository table data and
        put them in the cursor.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :returns: The return is the result of the desired query

        """
        cursor.execute('''SELECT * FROM repository;''')
        return cursor

    def get_wiki_modified(self, cursor, wiki_name):
        """ This is the method in charge of getting the datetime in the wiki was
        modified and put it in GMT format.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :param wiki_name: is the name of the current wiki.

        :returns: The return is the result of the desired query

        """
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + \
                       (MAX(wiki.time)/1000000) * INTERVAL '1s', \
                       name from wiki where(name=\'""" + wiki_name + """\') \
                       group by name; """)
        matriz_data_wiki = cursor.fetchall()
        modified_data = matriz_data_wiki[0][0]
        return modified_data

    def get_wiki_created(self, cursor, wiki_name):
        """ This is the method in charge of getting the datetime in the wiki was
        created and put it in GMT format.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :param wiki_name: is the name of the current wiki.

        :returns: The return is the result of the desired query

        """
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + \
                       (MIN(wiki.time)/1000000) * INTERVAL '1s', \
                       name from wiki where(name=\'""" + wiki_name + """\') \
                       group by name; """)
        matriz_data_wiki = cursor.fetchall()
        modified_data = matriz_data_wiki[0][0]
        return modified_data

    def get_attachment_created(self, cursor, attachment_id):
        """ This is the method in charge of getting the datetime in the
        attachment was created and put it in GMT format.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :param attachment_id: is the id of the current attachment.

        :returns: The return is the result of the desired query

        """
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + \
                       (MIN(attachment.time)/1000000) * INTERVAL '1s', \
                       id from attachment \
                       where(id=\'""" + attachment_id + """\') \
                       group by id; """)
        matriz_data_attachment = cursor.fetchall()
        modified_data = matriz_data_attachment[0][0]
        return modified_data

    def get_revision_created(self, cursor, revision):
        """ This is the method in charge of getting the datetime in the revision
        was modified and put it in GMT format.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :param revision: is the current revision.

        :returns: The return is the result of the desired query

        """
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + \
                       (MIN(revision.time)/1000000) * INTERVAL '1s', \
                       rev from revision where(rev=\'""" + revision + """\') \
                       group by rev; """)
        matriz_data_revision = cursor.fetchall()
        modified_data = matriz_data_revision[0][0]
        return modified_data

    def get_ticket_created(self, cursor, ticket_id):
        """ This is the method in charge of getting the datetime in the ticket
        was created and put it in GMT format.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :param ticket_id: is the id of the current ticket.

        :returns: The return is the result of the desired query

        """
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + \
                       (MIN(ticket.time)/1000000) * INTERVAL '1s', \
                       id from ticket where(id=""" + str(ticket_id) + """) \
                       group by id; """)
        matriz_data_ticket = cursor.fetchall()
        modified_data = matriz_data_ticket[0][0]
        return modified_data

    def get_ticket_modified(self, cursor, ticket_id):
        """ This is the method in charge of getting the datetime in the ticket
        was modified and put it in GMT format.

        :param cursor: A cursor coming from connections, it is necessary
            import the connections from library django.db, with it we can run
            sql commands.

        :param ticket_id: is the id of the current ticket.

        :returns: The return is the result of the desired query
        """
        cursor.execute("""SELECT TIMESTAMP WITH TIME ZONE 'epoch' + \
                       (MAX(ticket.time)/1000000) * INTERVAL '1s', \
                       id from ticket where(id=""" + str(ticket_id) + """) \
                       group by id; """)
        matriz_data_ticket = cursor.fetchall()
        modified_data = matriz_data_ticket[0][0]
        return modified_data
