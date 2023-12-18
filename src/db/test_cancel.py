import unittest
from DatabaseFunctions import DatabaseFunction
#ERRORED IMPORT, NEED FIXING
from datetime import datetime

class TestCancel(unittest.TestCase):
    """
    Test cases for the cancellation functionality of the Train Reservation System.
    """
    @classmethod
    def setUpClass(self):
        """
        Set up the necessary resources for testing the cancellation functionalities.
        """
        self.db = DatabaseFunction()

    def test_economy_cancel(self):
        """
        Test the cancellation of an economy class booking.
        """
        self.db.get_fare("Karachi", "Lahore", "economy")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "economy", "", "2002-09-17", 3, 0, 0, 0)

        doc = self.db.cancel_booking(3896, "1234567891011")

        expected = "The Booking has been cancelled"

        self.assertEqual(doc, expected)

    def test_business_cancel(self):
        """
        Test the cancellation of a business class booking.
        """
        self.db.get_fare("Karachi", "Lahore", "business")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "business", "A", "2002-09-17", 2, 0, 0, 0,)

        doc = self.db.cancel_booking(3896, "1234567891011")

        expected = "The Booking has been cancelled"

        self.assertEqual(doc, expected)

    def test_cancel_no_booking(self):
        """
        Test the case where no booking is found for cancellation.
        """
        doc = self.db.cancel_booking(4333, "2345678901011")

        expected = "No booking found with this cnic and bookingId"

        self.assertEqual(doc, expected)


    def test_invalid_booking_id(self):
        """
        Test cancellation with an invalid booking ID.
        """
        doc = self.db.cancel_booking(9999, "1234567891011")
        expected = "No booking found with this Booking ID and CNIC."
        self.assertEqual(doc, expected)

    def test_cancel_already_cancelled_booking(self):
        """
        Test cancellation of an already cancelled booking.
        """
        # Assume a booking is cancelled first
        self.db.get_fare("Karachi", "Lahore", "economy")
        self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "economy", "", "2002-09-17", 1, 0, 0, 0)
        self.db.cancel_booking(3896, "1234567891011")

        # Attempt to cancel the same booking again
        doc = self.db.cancel_booking(3896, "1234567891011")
        expected = "No booking found with this Booking ID and CNIC."
        self.assertEqual(doc, expected)


if __name__=="__main__":
    unittest.main()