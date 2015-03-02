"""
Test DataAPI class.
Objective: Test parameters and behavior.
"""
from colab.proxy.trac.data_api import TracDataAPI

from django.db import connections
from django.test import TestCase


class TracDataAPITest(TestCase):

    fixtures = ["trac_data.json"]

    def setUp(self):
        self.connection = connections['default']
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.connection.close()

    def test_dict_fetch_all(self):
        trac_dict = TracDataAPI()
        self.cursor.execute(''' SELECT * FROM trac_wiki;''')
        dict_result = trac_dict.dictfetchall(self.cursor)
        self.assertIn('collaborators', dict_result[0])

    def test_dict_fetch_all_is_dict(self):
        trac_dict = TracDataAPI()
        self.cursor.execute(''' SELECT * FROM trac_wiki;''')
        dict_result = trac_dict.dictfetchall(self.cursor)
        self.assertIsInstance(dict_result[0], dict)
