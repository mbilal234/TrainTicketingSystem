# from DatabaseConnection import db
#ERRORED IMPORT, NEED FIXING

from datetime import datetime, timedelta

class FillScheduleCollection:
    """
    This class fills the travels collection.

    The travels collection contains all the train departure times. This class has the functions for performing this task.

    Attributes:
        depts (list): A list of departure locations.
        arrival (list): A list of arrival locations.
        times (list): A list of departure times.
        dates (list): A list of dates for scheduling.
        start_date (datetime.date): The initial date for scheduling.
        t_num (int): Index for time slots.
        travel_id (int): The initial travel ID.
        travel_objects (list): List to store generated travel objects.

    Methods:
        generate_documents(): Generates a train schedule and writes it to the database.
        save_documents(): Saves the generated schedule in the database.
    """

    def __init__(self):
        """
        Initialize a FillScheduleCollection object.
        """
        self.depts = ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Peshawar"]
        self.arrival = ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Peshawar"]
        self.times = [
            "08:00:00", "16:00:00", "09:00:00", "17:00:00", "10:00:00", "18:00:00", "11:00:00", "19:00:00", "12:00:00",
            "20:00:00", "13:00:00", "21:00:00", "14:00:00", "22:00:00", "15:00:00", "23:00:00", "08:30:00", "16:30:00",
            "09:30:00", "17:30:00", "10:30:00", "18:30:00", "11:30:00", "19:30:00", "12:30:00", "20:30:00",
            "13:30:00", "21:30:00", "14:30:00", "22:30:00", "15:30:00", "23:30:00"
        ] * 100
        self.dates = []
        self.start_date = datetime.date(datetime.strptime("2023-10-14", "%Y-%m-%d"))
        for i in range(30):
            self.dates.append(self.start_date + timedelta(days=i))
        self.t_num = 0
        self.travel_id = 1000
        self.travel_objects = []

    def generate_documents(self):
        """
        Generates a train schedule and writes it to the database.

        The generated schedule includes information about departures and arrivals between different locations,
        including date and corresponding departure time.

        :param None:
        :type None:
        
        :return: None
        :rtype: None
        """

        for i in self.depts:
            for j in self.arrival:
                if i == j:
                    pass
                else:
                    for k in range(len(self.dates)):
                        timestamp = datetime.combine(self.dates[k], datetime.strptime(self.times[self.t_num], "%H:%M:%S").time())
                        self.travel_objects.append({"travelId": self.travel_id, "timestamp": str(timestamp), "departure": i, "destination": j})
                        self.t_num += 1
                        self.travel_id += 1
                        timestamp = datetime.combine(self.dates[k], datetime.strptime(self.times[self.t_num], "%H:%M:%S").time())
                        self.travel_objects.append({"travelId": self.travel_id, "timestamp": str(timestamp), "departure": i, "destination": j})
                        self.t_num += 1
                        self.travel_id += 1
                        if (self.t_num > 27): self.t_num = 0

    def save_documents(self):
        """
        Saves the generated train schedule in the database.

        :param None:
        :type None:
        
        :return: None
        :rtype: None
        """
        collection = db["schedule"]
        collection.insert_many(self.travel_objects)
        print("Documents Inserted into Database")                  
                    

if __name__ == "__main__":
    fsc = FillScheduleCollection()
    fsc.generate_documents()
    fsc.save_documents() 
