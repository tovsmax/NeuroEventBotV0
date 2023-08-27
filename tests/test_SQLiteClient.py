import unittest
from classes.SQLiteClient import SQLiteClient

class TestSQLiteClient(unittest.TestCase):
    def setUp(self) -> None:
        SQLiteClient._create_all_tables()
        
    def test_create_event_session(self):
        SQLiteClient.create_event_session()
        print(SQLiteClient.get_current_session())
        
        
if __name__ == '__main__':
    unittest.main()