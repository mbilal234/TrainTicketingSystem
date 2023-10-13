from DatabaseConnection import db   

class FillFaresCollection:
    """This class is built with the purpose of filling the fares collection in the database
    Fares are based on the cities between which the train is travelling.
    The class has two methods
    A generate_documents() method that will generate the fares
    And a save_documents() mathos that saves all the fares in the database
    """

    def __init__(self):
        self.cities = ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Peshawar"]
        self.fare_prices_economy = [3500, 3000, 2000, 4000, 1500, 2400, 1800, 2800, 1000, 3600]
        self.fare_prices_business = [6500, 5000, 4500, 8000, 3000, 3400, 3200, 5200, 2200, 7000]
        self.fare_num = 0
        self.fares = []

    def generate_documents(self):
        """This function will generate all the fares
        The function does not take any arguments and returns None
        The function generates objects that contain all the fares information
        The objects are then saved in self.fares list
        """

        for i in range(len(self.cities)):
            for j in range(i+1, len(self.cities)):
                self.fares.append({"firstCity": self.cities[i], "secondCity": self.cities[j], "class": "economy", "price": self.fare_prices_economy[self.fare_num]})
                self.fares.append({"firstCity": self.cities[i], "secondCity": self.cities[j], "class": "business", "price": self.fare_prices_business[self.fare_num]})
                self.fare_num += 1

    def save_documents(self):
        """After the fare prices have been stored in a list by the generate_fares() function
        This function is called to save all objects in the array to our database
        """
        collection = db["fares"]
        collection.insert_many(self.fares)
        print("Documents Inserted into Database") 


if __name__=="__main__":
    ffc = FillFaresCollection()
    ffc.generate_documents()
    ffc.save_documents()


        