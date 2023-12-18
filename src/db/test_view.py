import unittest
from DatabaseFunctions import DatabaseFunction
#ERRORED IMPORT NEED FIXING
from datetime import datetime

class TestView(unittest.TestCase):
    """
    Test cases for viewing bookings in the Train Reservation System.
    """
    @classmethod
    def setUpClass(self):
        """
        Set up the necessary resources for testing the view booking functionalities.
        """
        self.db = DatabaseFunction()

    @classmethod
    def tearDownClass(self):
        """
        Clean up resources after testing the view booking functionalities.
        """
        self.db.bookings.delete_one({"bookingId": 3896})
        self.db.seats.update_many({"bookingId": 3896}, {"$set":{"bookingId": None}})

        self.db.bookings.delete_one({"bookingId": 3897})
        self.db.seats.update_many({"bookingId": 3897}, {"$set":{"bookingId": None}})


    def test_view_booking_economy(self):
        """
        Test viewing details of an economy class booking.
        """
        self.db.get_fare("Karachi", "Lahore", "economy")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "economy", "", "2002-09-17", 3, 0, 0, 0)

        doc = self.db.view_booking(3897, "1234567891011")
        seats_booked = self.db.seats.find({"bookingId": 3897, "class": "economy"})
        seats = []
        for i in seats_booked:
            seats.append(i["seatNumber"])
        expected_doc = {
            "bookingId": 3897,
            "class": "economy",
            "timestamp": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "cnic": "1234567891011",
            "name": "Abdul Arham",
            "dateOfBirth": "2002-09-17",
            "travelId": 1000,
            "departure": "Karachi",
            "destination": "Lahore",
            "date": "2023-12-14",
            "time": "08:00",
            "numberOfSeats": 3,
            "numUnderTwo": 0,
            "numYoung": 0,
            "numAged": 0,
            "cost": 10500,
            "class": "economy",
            "seats": list(seats)
        }
        self.assertEqual(doc, expected_doc)

    def test_view_booking_business(self):
        """
        Test viewing details of a business class booking.
        """
        self.db.get_fare("Karachi", "Lahore", "business")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "business", "A", "2002-09-17", 2, 0, 0, 0)

        doc = self.db.view_booking(3896, "1234567891011")
        seats_booked = self.db.seats.find({"bookingId": 3896, "class": "business"})
        seats = []
        for i in seats_booked:
            seats.append(i["seatNumber"])
        expected_doc = {
            "bookingId": 3896,
            "timestamp": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "cnic": "1234567891011",
            "name": "Abdul Arham",
            "dateOfBirth": "2002-09-17",
            "travelId": 1000,
            "departure": "Karachi",
            "destination": "Lahore",
            "date": "2023-12-14",
            "time": "08:00",
            "numberOfSeats": 2,
            "numUnderTwo": 0,
            "numYoung": 0,
            "numAged": 0,
            "cost": 13000,
            "class": "business",
            "seats": list(seats)
        }
        self.assertEqual(doc, expected_doc)

    def test_view_when_no_booking(self):
        """
        Test the case where no booking is found for viewing.
        """
        doc = self.db.view_booking(4673, "1111111111111")
        expected = "No booking made with this Booking ID and CNIC."  
        self.assertEqual(doc, expected)


    def test_view_invalid_booking_id(self):
        """
        Test viewing details with an invalid booking ID.
        """
        doc = self.db.view_booking(9999, "1234567891011")
        expected = "No booking made with this Booking ID and CNIC."
        self.assertEqual(doc, expected)

    def test_view_invalid_booking_id(self):
        """
        Test viewing details with an invalid booking ID.
        """
        doc = self.db.view_booking(9999, "1234567891011")
        expected = "No booking made with this Booking ID and CNIC."
        self.assertEqual(doc, expected)

    def test_view_invalid_cnic(self):
        """
        Test viewing details with an invalid CNIC.
        """
        doc = self.db.view_booking(3896, "invalid_cnic")
        expected = "No booking made with this Booking ID and CNIC."
        self.assertEqual(doc, expected)


if __name__=="__main__":
    unittest.main()