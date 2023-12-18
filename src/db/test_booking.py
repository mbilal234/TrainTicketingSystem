import unittest.result
import DatabaseFunctions as db
#NEED FIXING, ERROR IMPORT
import unittest
from datetime import datetime

class TestBooking(unittest.TestCase):
    """
    Test cases for the booking functionality of the Train Reservation System.
    """

    @classmethod
    def setUpClass(self):
        """
        Set up the necessary resources for testing the booking functionalities.
        """
        self.db = db.DatabaseFunction()

    @classmethod
    def tearDownClass(self):
        """
        Clean up resources after testing the booking functionalities.
        """
        self.db.bookings.delete_one({"bookingId": 3896})
        self.db.seats.update_many({"bookingId": 3896}, {"$set":{"bookingId": None}})

        self.db.bookings.delete_one({"bookingId": 3897})
        self.db.seats.update_many({"bookingId": 3897}, {"$set":{"bookingId": None}})

    def test_fare(self):
        """
        Test fare calculation for different routes and classes.
        """
        fare = self.db.get_fare("Karachi", "Lahore", "economy")
        self.assertEqual(fare, 3500)

        fare = self.db.get_fare("Peshawar", "Rawalpindi", "economy")
        self.assertEqual(fare, 1000)

        fare = self.db.get_fare("Quetta", "Lahore", "economy")
        self.assertEqual(fare, 2400)

        fare = self.db.get_fare("Karachi", "Lahore", "business")
        self.assertEqual(fare, 6500)

        fare = self.db.get_fare("Peshawar", "Rawalpindi", "business")
        self.assertEqual(fare, 2200)

        fare = self.db.get_fare("Quetta", "Lahore", "business")
        self.assertEqual(fare, 3400)

    def test_get_seats_and_time(self):
        """
        Test the retrieval of available seats and departure times for different routes and classes.

        The trains used in this test case have all free seats for the given time.
        """ 
        seats_and_time = self.db.get_seats_and_time("Karachi", "Rawalpindi", "2023-12-24", "08:00", "economy")
        economy_seats = self.db.seats.find({"travelId": 1080, "class":"economy"})
        expected_result = {"suggested":"2023-12-24 12:30:00", "times": {"2023-12-24 12:30:00": 1080, "2023-12-24 20:30:00":1081}, "seats":list(economy_seats)}
        self.assertEqual(seats_and_time, expected_result)

        seats_and_time = self.db.get_seats_and_time("Lahore", "Peshawar", "2023-12-31", "13:30", "economy")
        economy_seats = self.db.seats.find({"travelId": 1454, "class":"economy"})
        actual_result = {"suggested":"2023-12-31 11:00:00", "times": {"2023-12-31 11:00:00": 1454, "2023-12-31 19:00:00":1455}, "seats":list(economy_seats)}
        self.assertEqual(seats_and_time, actual_result)

        seats_and_time = self.db.get_seats_and_time("Peshawar", "Quetta", "2024-01-09", "12:00", "economy")
        economy_seats = self.db.seats.find({"travelId": 2192, "class":"economy"})
        actual_result = {"suggested":"2024-01-09 08:30:00", "times": {"2024-01-09 08:30:00": 2192, "2024-01-09 16:30:00":2193}, "seats":list(economy_seats)}
        self.assertEqual(seats_and_time, actual_result)

    def test_get_business_seats(self):
        """
        Test the retrieval of available business class seats for different routes.
        """
        economy_seats = []
        for i in range(100):
            economy_seats.append(str(i+1))

        """
        The trains we are using in this test case
        has all free seats for the given time
        """
            
        seats = self.db.get_business_seats(1080, "A")
        actual_result = {"seats":['A2', 'A6', 'A1', 'A4', 'A5', 'A3']}
        self.assertEqual(seats, actual_result)

        seats = self.db.get_business_seats(1455, "C")
        actual_result = {"seats":['C2', 'C4', 'C3', 'C6', 'C5', 'C1']}
        self.assertEqual(seats, actual_result)

        seats = self.db.get_business_seats(2193, "F")
        actual_result = {"seats":['F1', 'F4', 'F2', 'F3', 'F5', 'F6']}
        self.assertEqual(seats, actual_result)  

    def test_economy_booking(self):

        """Now we are going to make a booking, we know the seats are available"""

        self.db.get_fare("Karachi", "Lahore", "economy")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "economy", "", "2002-09-17", 3, 0, 0, 0)
        expected = 3897
        self.assertEqual(doc, expected)

    def test_business_booking(self):
        """
        Test the booking of business class seats.
        """
        self.db.get_fare("Karachi", "Lahore", "business")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "business", "A", "2002-09-17", 2, 0, 0, 0)
        expected = 3896
        self.assertEqual(doc, expected)

    def test_invalid_fare(self):
        """
        Test fare calculation for invalid routes or classes.
        """
        # Test for an invalid route
        fare = self.db.get_fare("InvalidCity1", "InvalidCity2", "economy")
        self.assertEqual(fare, "No Departure City Specified")

        # Test for an invalid class
        fare = self.db.get_fare("Karachi", "Lahore", "invalid_class")
        self.assertEqual(fare, "No Class Type Specified")

    def test_insufficient_seats(self):
        """
        Test booking when there are insufficient seats available.
        """
        # Assuming there are only 2 economy seats available for this test
        self.db.get_fare("Karachi", "Lahore", "economy")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "economy", "", "2002-09-17", 3, 0, 0, 0)
        expected = "Not Enough Seats Available"
        self.assertEqual(doc, expected)

    def test_invalid_seats_and_time(self):
        """
        Test the retrieval of seats and departure times for invalid routes or classes.
        """
        # Test for an invalid departure city
        seats_and_time = self.db.get_seats_and_time("InvalidCity", "Lahore", "2023-12-24", "08:00", "economy")
        self.assertEqual(seats_and_time, "No Departure City Specified")

        # Test for an invalid destination city
        seats_and_time = self.db.get_seats_and_time("Karachi", "InvalidCity", "2023-12-24", "08:00", "economy")
        self.assertEqual(seats_and_time, "No Destination City Specified")


if __name__=="__main__":
    unittest.main()