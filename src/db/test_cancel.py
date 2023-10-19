import unittest
# from DatabaseFunctions import DatabaseFunction
#ERRORED IMPORT, NEED FIXING
from datetime import datetime

class TestCancel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DatabaseFunction()

    def test_economy_cancel(self):
        self.db.get_fare("Karachi", "Lahore", "economy")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["1", "2", "3"])

        doc = self.db.cancel_booking(3896, "1234567891011")

        expected = "The Booking has been cancelled"

        self.assertEqual(doc, expected)

    def test_business_cancel(self):
        self.db.get_fare("Karachi", "Lahore", "business")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["A1", "A2"])

        doc = self.db.cancel_booking(3896, "1234567891011")

        expected = "The Booking has been cancelled"

        self.assertEqual(doc, expected)

    def test_cancel_no_booking(self):
        doc = self.db.cancel_booking(4333, "2345678901011")

        expected = "No booking found with this cnic and bookingId"

        self.assertEqual(doc, expected)


if __name__=="__main__":
    unittest.main()