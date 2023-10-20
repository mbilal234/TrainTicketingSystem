import unittest
# from DatabaseFunctions import DatabaseFunction
#ERRORED IMPORT NEED FIXING
from datetime import datetime

class TestView(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = DatabaseFunction()

    @classmethod
    def tearDownClass(self):
        self.db.bookings.delete_one({"bookingId": 3896})
        self.db.seats.update_many({"bookingId": 3896}, {"$set":{"bookingId": None}})

        self.db.bookings.delete_one({"bookingId": 3897})
        self.db.seats.update_many({"bookingId": 3897}, {"$set":{"bookingId": None}})


    def test_view_booking_economy(self):

        self.db.get_fare("Karachi", "Lahore", "economy")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["1", "2", "3"])

        doc = self.db.view_booking(3897, "1234567891011")
        expected_doc = {
            "bookingId": 3897,
            "timestamp": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "cnic": "1234567891011",
            "name": "Abdul Arham",
            "dateOfBirth": "2002-09-17",
            "travelId": 1000,
            "departure": "Karachi",
            "destination": "Lahore",
            "numberOfSeats": 3,
            "numUnderTwo": 0,
            "numYoung": 0,
            "numAged": 0,
            "cost": 10500,
            "seats": ["1", "2", "3"]
        }
        self.assertEqual(doc, expected_doc)

    def test_view_booking_business(self):
        self.db.get_fare("Karachi", "Lahore", "business")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["A1", "A2"])

        doc = self.db.view_booking(3896, "1234567891011")
        expected_doc = {
            "bookingId": 3896,
            "timestamp": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "cnic": "1234567891011",
            "name": "Abdul Arham",
            "dateOfBirth": "2002-09-17",
            "travelId": 1000,
            "departure": "Karachi",
            "destination": "Lahore",
            "numberOfSeats": 2,
            "numUnderTwo": 0,
            "numYoung": 0,
            "numAged": 0,
            "cost": 13000,
            "seats": ["A1", "A2"]
        }
        self.assertEqual(doc, expected_doc)

    def test_view_when_no_booking(self):
        doc = self.db.view_booking(4673, "1111111111111")
        expected = "No booking made with this Booking ID and CNIC."  
        self.assertEqual(doc, expected)


if __name__=="__main__":
    unittest.main()