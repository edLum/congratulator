import unittest

import sqlalchemy

from utils.db_conn import engine
from utils.sql_interface import SqlExecutioner
from exporter import InteractionsExporter, ChangesExporter

class TestSqlExecutioner(unittest.TestCase):

    def setUp(self):
        self.sql_exec = SqlExecutioner(engine)
        self.test_run_query = "SELECT * FROM tfrresults;"
        self.sql_exec.connect_to_db()

    def test_connect_to_db(self):
        self.assertIsInstance(self.sql_exec.conn, sqlalchemy.engine.base.Connection)

    def test_run_query(self):
        self.assertTrue(self.sql_exec.run(self.test_run_query))

    def test_query_results(self):
        self.assertIsNotNone(self.sql_exec.get_query_results(self.test_run_query))
        

class TestCsvHandler(unittest.TestCase):

    def setUp(self):
        pass

class TestTfrExporter(unittest.TestCase):

    def setUp(self):
        self.exporter_changes = ChangesExporter()
        self.exporter_interactions = InteractionsExporter()

    def test_interactions(self):
        pass

class TestTfrImporter(unittest.TestCase):

    def setUp(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSqlExecutioner)
    unittest.TextTestRunner(verbosity=2).run(suite)
           
