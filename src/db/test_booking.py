import unittest.result
# import DatabaseFunctions as db
#NEED FIXING, ERROR IMPORT
import unittest
from datetime import datetime

class TestBooking(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db = db.DatabaseFunction()

    @classmethod
    def tearDownClass(self):
        self.db.bookings.delete_one({"bookingId": 3896})
        self.db.seats.update_many({"bookingId": 3896}, {"$set":{"bookingId": None}})

        self.db.bookings.delete_one({"bookingId": 3897})
        self.db.seats.update_many({"bookingId": 3897}, {"$set":{"bookingId": None}})

    def test_fare(self):
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

        economy_seats = []
        for i in range(100):
            economy_seats.append(str(i+1))

        """
        The trains we are using in this test case
        has all free seats for the given time
        """
            
        seats_and_time = self.db.get_seats_and_time("Karachi", "Rawalpindi", "2023-10-24", "08:00:00", "economy")
        actual_result = {"times": {"2023-10-24 12:30:00": 1080, "2023-10-24 20:30:00":1081}, "seats":economy_seats}
        self.assertEqual(seats_and_time, actual_result)

        seats_and_time = self.db.get_seats_and_time("Lahore", "Peshawar", "2023-10-31", "13:30:00", "economy")
        actual_result = {"times": {"2023-10-31 11:00:00": 1454, "2023-10-31 19:00:00":1455}, "seats":economy_seats}
        self.assertEqual(seats_and_time, actual_result)

        seats_and_time = self.db.get_seats_and_time("Peshawar", "Quetta", "2023-11-09", "12:00:00", "business")
        actual_result = {"times": {"2023-11-09 08:30:00": 2192, "2023-11-09 16:30:00":2193}, "seats":[]}
        self.assertEqual(seats_and_time, actual_result)

    def test_get_business_seats(self):

        economy_seats = []
        for i in range(100):
            economy_seats.append(str(i+1))

        """
        The trains we are using in this test case
        has all free seats for the given time
        """
            
        seats = self.db.get_business_seats(1080, "A")
        actual_result = {"seats":["A1", "A2", "A3", "A4", "A5", "A6"]}
        self.assertEqual(seats, actual_result)

        seats = self.db.get_business_seats(1455, "C")
        actual_result = {"seats":["C1", "C2", "C3", "C4", "C5", "C6"]}
        self.assertEqual(seats, actual_result)

        seats = self.db.get_business_seats(2193, "F")
        actual_result = {"seats":["F1", "F2", "F3", "F4", "F5", "F6"]}
        self.assertEqual(seats, actual_result)

    def test_economy_booking(self):

        """Now we are going to make a booking, we know the seats are available"""

        self.db.get_fare("Karachi", "Lahore", "economy")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["1", "2", "3"])
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

    def test_business_booking(self):

        self.db.get_fare("Karachi", "Lahore", "business")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["A1", "A2"])
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

    def test_economy_seats_already_booked(self):
        self.db.get_fare("Karachi", "Lahore", "economy")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["1", "2", "3"])

        expected = "The Seat 1 is already booked."

        self.assertEqual(doc, expected)

    def test_business_seats_already_booked(self):
        self.db.get_fare("Karachi", "Lahore", "economy")

        doc = self.db.book_ticket("1234567891011", "Abdul Arham", 1000, "2002-09-17", 0, 0, 0, ["A1", "A2", "A3"])

        expected = "The Seat A1 is already booked."

        self.assertEqual(doc, expected)


if __name__=="__main__":
    unittest.main()