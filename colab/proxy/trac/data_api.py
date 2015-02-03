from colab.proxy.utils.proxy_data_api import ProxyDataAPI
import time
from django.db import connections
from colab.proxy.trac.models import Attachment, Revision, Ticket, Wiki
from django.utils import timezone


class TracDataAPI(ProxyDataAPI):

    def fetch_data(self):
        attachment = Attachment()
        revision = Revision()
        ticket = Ticket()
        connection = connections['trac']
        cursor = connection.cursor()
        self.fetch_data_wiki(cursor)
        
    def fetch_data_wiki(self, cursor):
        wiki = Wiki()
        cursor.execute('''SELECT * FROM wiki;''')
        wiki_dict = self.dictfetchall(cursor)
        collaborators = []

        for line in wiki_dict:
            wiki.name = line['name']
            wiki.text = line['text']
            wiki.author = line['author']
            if line['author'] not in collaborators:
                    collaborators.append(line['author'])
            wiki.collaborators = collaborators
            local_time = line['time']/1000000
            wiki.created = time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.localtime(local_time))
            wiki.modified = str(timezone.now())
            wiki.modified_by = wiki.author 
            wiki.save()

    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
         ]   
