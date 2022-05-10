import unittest
from app import app
from database.db import db  
  
class BaseCase(unittest.TestCase):  
    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()


    def tearDown(self):
        #limpa nossa infra de teste, inclusive banco
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)