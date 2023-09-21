import json
from peripheries import Train
import os
class TrainsMaker:
    def __init__(self):
        self.depts = ["karachi", "lahore", "rawalpindi", "quetta", "peshawar"]
        self.arrival = ["karachi", "lahore", "rawalpindi", "quetta", "peshawar"]
        self.days = ["MON", "MON", "TUE", "TUE", "WED", "WED", "THU", "THU", "FRI", "FRI", "SAT", "SAT", "SUN", "SUN"]
        self.types = ["economy", "business"]
        self.id = 1001
        self.times = [
            "0800", "1600", "0900", "1700", "1000", "1800", "1100", "1900", "1200", "2000", "1300", "2100", "1400",
            "2200", "1500", "2300", "0830", "1630", "0930", "1730", "1030", "1830", "1130", "1930", "1230", "2030",
            "1330", "2130", "1430", "2230", "1530", "2330"
        ] * 100
        self.t_num = 0

    def generate_train_objects(self):
        train_objects = []

        for departure in self.depts:
            for arrival in self.arrival:
                if departure != arrival:
                    for day in self.days:
                        for train_type in self.types:
                            train_id = self.id
                            time = self.times[self.t_num]
                            seats = self.get_seats(train_type)
                            train = Train.Train(train_id, train_type, day, time, departure, arrival, seats)
                            train_objects.append(train)
                            self.id += 1
                            self.t_num += 1

        return train_objects

    def get_seats(self, train_type):
        if train_type == "economy":
            return {
                str(i): True for i in range(1, 31)
            }
        elif train_type == "business":
            return {
                f"{class_letter}{i}": True for class_letter in ["A", "B", "C", "D", "E"] for i in range(1, 7)
            }

    def save_trains_to_file(self, train_objects):
        # Define the data directory path (assuming it's at the same level as 'src')
        data_directory = os.path.join(os.getcwd(), '..', 'data')
        
        # Ensure the 'data' directory exists, create it if it doesn't
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        
        # Define the file path for Trains.txt
        trains_txt_path = os.path.join(data_directory, 'Trains.txt')

        with open(trains_txt_path, "w") as file:
            for train in train_objects:
                train_data = train.to_json()
                json.dump(train_data, file)
                file.write("\n")








