import unittest.result
import DatabaseFunctions as db
#NEED FIXING, ERROR IMPORT
import unittest
from datetime import datetime
import DatabaseConnection

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
        self.dc = DatabaseConnection.connect()

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
        berth = "A"
        pattern = f"^{berth}"
        actual_result = {"seats": list(self.dc["seats"].find({"class": "business", "travelId": 1080, "seatNumber": { "$regex": pattern, "$options": "i"}}))}
        self.assertEqual(seats, actual_result)

        seats = self.db.get_business_seats(1455, "C")
        berth = "C"
        pattern = f"^{berth}"
        actual_result = {"seats":list(self.dc["seats"].find({"class": "business", "travelId": 1455, "seatNumber": { "$regex": pattern, "$options": "i"}}))}
        self.assertEqual(seats, actual_result)

        seats = self.db.get_business_seats(2193, "F")
        berth = "F"
        pattern = f"^{berth}"
        actual_result = {"seats":list(self.dc["seats"].find({"class": "business", "travelId": 2193, "seatNumber": { "$regex": pattern, "$options": "i"}}))}
        self.assertEqual(seats, actual_result)  

    def test_economy_booking(self):

        """Now we are going to make a booking, we know the seats are available"""

        self.db.get_fare("Karachi", "Lahore", "economy")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 3, 0, 0, 0, "economy")
        expected = 3897
        self.assertEqual(doc, expected)

    def test_business_booking(self):
        """
        Test the booking of business class seats.
        """
        self.db.get_fare("Karachi", "Lahore", "business")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 2, 0, 0, 0, "business", "A")
        expected = 3896
        self.assertEqual(doc, expected)


if __name__=="__main__":
    unittest.main()