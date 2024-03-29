from datetime import datetime
try:
    import DatabaseConnection
except:
    from db import DatabaseConnection


# import DatabaseConnection
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

    def get_fare(self, departure, destination,class_type):

        """
        The function gets the fare from the database based on the departure and arrival cities selected
        """

        if not departure:
            return "No Departure City Specified"
        
        if not destination:
            return "No Destination City Specified"
        
        if not class_type:
             return "No Class Type Specified"

        fare_query = {"$and": [{"$or": [{"firstCity": departure, "secondCity": destination }, {"firstCity": destination, "secondCity": departure}]}, {"class": class_type}]}
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
        #CURRENT ISSUE IS THAT DATE ON GUI IS UPTILL 2022, while in DATABASE IT IS AFTER 2023
        documents = list(self.schedule.find(query))
        # print("The documents are ", type(documents), len(documents))

        if len(documents) == 0:
            print("No Trains Found")
            return "No Trains Found"
        
        time_object = datetime.strptime(str(date)+" "+time+":00", "%Y-%m-%d %H:%M:%S")
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

        return {"suggested": str(suggested_time),"times": {str(suggested_time): travel_id_1, str(second_option_time): travel_id_2}, "seats": all_seats}
    

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
    
    def get_economy_seats(self, travelId):

        """
        The function aims to fetch business class seats
        The seats from the berth given in argument is fetched
        The function takes travelId and berth in arguments which are used in query
        This function returns a list of seats to suggest the user
        """

        if not travelId:
            return "No Travel ID Specified"

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
                    "seats.class": "economy",
                    "seats.bookingId": None
                }
            }
        ]))

        all_seats = []
        for i in seats:
            all_seats.append(i["seats"])

        return {"seats": all_seats}
    
    def book_ticket(self, cnic, name, travelId, dateOfBirth, numUnderTwo, numYoung, numAged, num_of_seats, travelling_class, berth=None):

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

        other_seats = num_of_seats - numUnderTwo - numYoung - numAged

        try:
            cost = int(other_seats * self.fare + numUnderTwo * self.fare * 0.7 + numYoung * self.fare * 0.8 + numAged * self.fare * 0.75)
        except:
            cost = 3000

        if travelling_class=="economy":
            seats = list(self.seats.find({"class": travelling_class, "travelId": travelId, "bookingId": None}))
        else:
            pattern = f"^{berth}"
            seats = list(self.seats.find({"class": travelling_class, "travelId": travelId, "bookingId": None, "seatNumber": { "$regex": pattern, "$options": "i"},}))

        n = len(seats)
        print("dbjknfjvkjfnkuscJK,rnoinuihfifiuwfeaoivbjneilhvbjk")
        print(n)

        if n < num_of_seats:
            return "Not Enough Seats Available"

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
        
        for i in range(num_of_seats):
            self.seats.update_one({"seatNumber":seats[i]["seatNumber"], "travelId": travelId}, {"$set": {"bookingId": bookingId}})

        self.bookings.insert_one(booking_document)

        return bookingId


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
        if booking == None:
            return None
        
        seats = []
        seat_type = ""
        if booking:
            all_seats = self.seats.find({"bookingId": bookingId})
            for i in all_seats:
                if seat_type == "":
                    seat_type = i["class"]
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
            "date": train_reserved["timestamp"].split(" ")[0],
            "time": train_reserved["timestamp"].split(" ")[1][:-3],
            "numberOfSeats" : booking["numberOfSeats"],
            "numUnderTwo": booking["numUnderTwo"],
            "numYoung": booking["numYoung"],
            "numAged": booking["numAged"],
            "cost": booking["cost"],
            "class": seat_type,
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
    # df = DatabaseFunction()
    # info = df.get_fare("Karachi", "Lahore", "economy")
    # info = df.get_seats_and_time("Karachi", "Lahore", "2023-10-23", "08:30:00", "economy")
    # print("Final info is:\n")
    # print(info)

    # To make sure that you have got the correct suggested times, run this code
    # print(info["times"]) # The times suggested, the keys show the time while the values are the travelIds
    # get_docs = df.schedule.find({"departure": "Karachi", "destination": "Lahore", "timestamp": { "$regex": "^2023-10-14", "$options": "i"}})
    # for i in get_docs:
    #     print(i)

    # Code for Booking
    # doc = df.book_ticket("////////////////", "Abdul Arham", 1000,  "business", "A", "2002-09-17", 0, 0, 0, 1)
    # print(doc)

    # Code for viewing
    # booking = df.view_booking(3897, "1111111111112")
    # print(booking)

    # Code for cancelling
    # result = df.cancel_booking(3896, "//////////")
    # print(result)

    df = DatabaseFunction()

    doc = df.book_ticket("3830342091289", "Abdul Arham", 1254, "2002-09-17", 0, 0, 0, 2, "economy")
    print(doc)

    db = DatabaseConnection.connect()
    seats_collection = db["seats"]
    seats = list(seats_collection.find({"class": "economy", "travelId": 1000, "bookingId": None}))
    for i in seats:
        if i["bookingId"] is not None:
            print("Hello World")


