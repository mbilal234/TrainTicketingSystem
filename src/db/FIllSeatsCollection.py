from DatabaseConnection import db

class FillSeatsCollection:

    """
    The FillSeatsCollection class will add documents to the seat collection in database
    The class has two functions
    - One is the generate documents function that will generate all the documents
    - The second function is the save_documents() function that will save the documents in database
    """

    def __init__(self):
        collection = db["schedule"]
        self.complete_schedule = collection.find()
        self.seats = []
        
    def generate_documents(self):
        
        """
        This function will generate all documents
        The document will have information about the seat number, class and the travelId
        """

        for i in self.complete_schedule:
            for j in range(1, 101):
                self.seats.append({"class": "economy", "seatNumber": str(j), "travelId": i["travelId"], "bookingId": None})
            for j in range(6):
                for k in range(6):
                    self.seats.append({"class": "business", "seatNumber": chr(65+j)+str(k+1), "travelId": i["travelId"], "bookingId": None})

    def save_documents(self):
        """
        After the generation of all the seats documents
        This function saves the documents in the database
        """
        collection = db["seats"]
        collection.insert_many(self.seats)
        print("Documents Inserted into Database") 

if __name__=="__main__":
    fsc = FillSeatsCollection()
    fsc.generate_documents()
    fsc.save_documents() 
