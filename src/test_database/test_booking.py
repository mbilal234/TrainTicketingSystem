import unittest
from src import db
# from db import DatabaseFunctions

class TestBooking(unittest.TestCase):

    def __init__(self):
        self.db = db.DatabaseFunctions()

    def test_fare(self):
        fare = self.db.get_fare("Karachi", "Lahore")
        self.assertEqual(fare, 3500)

if __name__=="__main__":
    unittest.main()