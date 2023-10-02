from datetime import datetime
from db import DatabaseConnection
class DatabaseFunction:

    """
    This class contains all the database functionality
    The main aim of the class is to provide function for data storage and retrieval
    The class currently has four functions
    The get_fare() function fetches the fare from the database
    Fares have been set based on the departure and arrival cities
    The get_seats_and_time() function fetches all the seats for economy class and provides the suggested timings
    The get_business_seats() fetches the seats from database based on the selected berth
    The book_ticket() function completes the booking process
    """

    def __init__(self):
        db = DatabaseConnection.connect()
        self.fares = db["fares"]
        self.schedule = db["schedule"]
        self.bookings = db["bookings"]  
        self.seats = db["seats"]
        self.fare = None

    def get_fare(self, departure, destination):

        """
        The function gets the fare from the database based on the departure and arrival cities selected
        """

        if not departure:
            return "No Departure City Specified"
        
        if not destination:
            return "No Destination City Specified"

        fare_query = {"$or": [{"firstCity": departure, "secondCity": destination }, {"firstCity": destination, "secondCity": departure}]}
        self.fare = int(self.fares.find(fare_query)[0]["price"])
        return self.fare

    def get_seats_and_time(self, departure, destination, date, time, travelling_class):

        """
        The function has the aim to suggest the user with the nearest timing to the selected one
        The function returns the remaining seats in train if case the user is travelling in economy class
        The business class seats are suggested on the basis of berth and is handled in another function
        The function takes departure, destination, date, time and the travelling_class in arguments
        The function returns a dictionary and a list 
        The dictionary has the suggested times in their keys with the travelIds as values
        The returned list has the suggested seats for the user or the remaining free seats
        """
        if not departure:
            return "No Departure City Specified"

        if not destination:
            return "No Destination City Specified"

        if not date:
            return "No Departure Date Specified"
        
        if not time:
            return "No Departure Time Specified"
        
        if not travelling_class:
            return "No Travelling Class Specified"
        
        pattern = f"^{date}"
        query = { "departure": departure, "destination": destination, "timestamp": { "$regex": pattern, "$options": "i"}}
        documents = self.schedule.find(query)

        time_object = datetime.strptime(date+" "+time, "%Y-%m-%d %H:%M:%S")
        first_shift_time = datetime.strptime(documents[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
        second_shift_time = datetime.strptime(documents[1]["timestamp"], "%Y-%m-%d %H:%M:%S")

        if abs(first_shift_time - time_object) < abs(second_shift_time - time_object):
            suggested_time = first_shift_time
            second_option_time = second_shift_time
            travel_id_1 = documents[0]["travelId"]
            travel_id_2 = documents[1]["travelId"]
        else:
            suggested_time = second_shift_time
            second_option_time = first_shift_time
            travel_id_2 = documents[0]["travelId"]
            travel_id_1 = documents[1]["travelId"]
        
        seats = list(self.schedule.aggregate([
            {
                "$match": {
                    "timestamp": str(suggested_time),
                    "departure": departure,
                    "destination": destination
                }
            },
            {
                "$lookup": {
                    "from": "seats",
                    "localField": "travelId",
                    "foreignField": "travelId",
                    "as": "seats"
                }
            },
            {
                "$unwind": "$seats"
            },
            {
                "$match": {
                    "seats.class": travelling_class if travelling_class == "economy" else "",
                    "seats.bookingId": None
                }
            }
        ]))

        all_seats = []
        for i in seats:
            all_seats.append(i["seats"])

        return {"times": {str(suggested_time): travel_id_1, str(second_option_time): travel_id_2}, "seats": all_seats}
    

    def get_business_seats(self, travelId, berth):

        """
        The function aims to fetch business class seats
        The seats from the berth given in argument is fetched
        The function takes travelId and berth in arguments which are used in query
        This function returns a list of seats to suggest the user
        """

        if not travelId:
            return "No Travel ID Specified"
        
        if not berth:
            return "No Berth Specified"
        
        pattern = f"^{berth}"

        seats = list(self.schedule.aggregate([
            {
                "$match": {
                    "travelId": travelId
                }
            },
            {
                "$lookup": {
                    "from": "seats",
                    "localField": "travelId",
                    "foreignField": "travelId",
                    "as": "seats"
                }
            },
            {
                "$unwind": "$seats"
            },
            {
                "$match": {
                    "seats.class": "business",
                    "seats.seatNumber": { "$regex": pattern, "$options": "i"},
                    "seats.bookingId": None
                }
            }
        ]))

        all_seats = []
        for i in seats:
            all_seats.append(i["seats"])

        return {"seats": all_seats}
    
    def book_ticket(self, cnic, name, travelId, dateOfBirth, numUnderTwo, numYoung, numAged, seats):

        """
        This function completes the booking procedure
        The function takes some arguments and store them in database
        The function also updates the status of the seats booked by the user
        The function does not return anything
        """

        if not cnic:
            return "No CNIC Number Specified"
        
        if not name:
            return "No Name Specified"
        
        if not travelId:
            return "No Travel ID Specified"
        
        if not dateOfBirth:
            return "No Date Of Birth Specified"
        
        num_of_seats = len(seats)

        other_seats = num_of_seats - numUnderTwo - numYoung - numAged

        try: #cost function is not working properly!
            cost = int(other_seats * self.fare + numUnderTwo * self.fare * 0.7 + numYoung * self.fare * 0.8 + numAged * self.fare * 0.75)
        except:
            cost = 3000

        bookings_pointer = self.bookings.count_documents({})

        bookingId = 3896 + bookings_pointer

        booking_document = {
            "bookingId": bookingId, 
            "timestamp": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "cnic": cnic,
            "name": name,
            "dateOfBirth": dateOfBirth,
            "travelId": travelId,
            "numberOfSeats" : num_of_seats,
            "numUnderTwo": numUnderTwo,
            "numYoung": numYoung,
            "numAged": numAged,
            "cost": cost
            }
        
        for i in seats:
            seat_document = self.seats.find_one({"seatNumber": i})
            if seat_document["bookingId"]:
                return "The Seat "+str(i)+" is already booked."
        
        self.bookings.insert_one(booking_document)

        for i in seats:
            self.seats.update_one({"seatNumber": i}, {"$set":{"bookingId": bookingId}})


    def view_booking(self, bookingId, cnic):
        """
        The function is aimed for displaying the booking to the user
        The function takes the bookingId and cnic and matches the documents in the database
        """

        if not bookingId:
            return "No Booking ID Specified"
        
        if not cnic:
            return "No CNIC Number Specified"

        booking = self.bookings.find_one({"bookingId": bookingId, "cnic": cnic})
        seats = []
        if booking:
            all_seats = self.seats.find({"bookingId": bookingId})
            for i in all_seats:
                seats.append(i["seatNumber"])  

        train_reserved = self.schedule.find_one({"travelId": booking["travelId"]})

        view_document = {
            "bookingId": bookingId, 
            "timestamp": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "cnic": cnic,
            "name": booking["name"],
            "dateOfBirth": booking["dateOfBirth"],
            "travelId": booking["travelId"],
            "departure": train_reserved["departure"],
            "destination": train_reserved["destination"],
            "numberOfSeats" : booking["numberOfSeats"],
            "numUnderTwo": booking["numUnderTwo"],
            "numYoung": booking["numYoung"],
            "numAged": booking["numAged"],
            "cost": booking["cost"],
            "seats": seats,
        }

        return view_document

    def cancel_booking(self, bookingId, cnic):
        """
        This function works to cancel booking
        The function takes the bookingId and cnic and matches the documents in the database
        """    

        if not bookingId:
            return "No Booking ID Specified"
        
        if not cnic:
            return "No CNIC Number Specified"

        booking = self.bookings.find_one({"bookingId": bookingId, "cnic": cnic})
        if booking is None:
            return "No booking found with this cnic and bookingId"

        self.bookings.delete_one({"bookingId": bookingId, "cnic": cnic})
        self.seats.update_many({"bookingId": bookingId}, {"$set":{"bookingId": None}})

        return "The Booking has been cancelled"
        

if __name__=="__main__":
    df = DatabaseFunction()
    df.get_fare("Karachi", "")
    info = df.get_seats_and_time("Karachi", "Lahore", "2023-10-23", "08:30:00", "economy")


    # To make sure that you have got the correct suggested times, run this code
    # print(info["times"]) # The times suggested, the keys show the time while the values are the travelIds
    # get_docs = df.schedule.find({"departure": "Karachi", "destination": "Lahore", "timestamp": { "$regex": "^2023-10-14", "$options": "i"}})
    # for i in get_docs:
    #     print(i)

    # Code for Booking
    # doc = df.book_ticket("/////////", "///////////", 1000, "2002-09-17", 0, 0, 0, [1])
    # print(doc)

    # Code for viewing
    # booking = df.view_booking(3896, "///////////")
    # print(booking)

    # Code for cancelling
    # result = df.cancel_booking(3896, "//////////")
    # print(result)


