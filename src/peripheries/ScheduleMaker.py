import os

class ScheduleMaker:
    def __init__(self):
        self.schedule = []
        self.depts = ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Peshawar"]
        self.arrival = ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Peshawar"]
        self.days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        self.times = [
            "0800", "1600", "0900", "1700", "1000", "1800", "1100", "1900", "1200", "2000", "1300", "2100", "1400",
            "2200", "1500", "2300", "0830", "1630", "0930", "1730", "1030", "1830", "1130", "1930", "1230", "2030",
            "1330", "2130", "1430", "2230", "1530", "2330"
        ] * 100
        self.t_num = 0

    def generate_schedule(self):
        # Define the data directory path (assuming it's at the same level as 'src')
        data_directory = os.path.join(os.getcwd(), 'data')
        
        # Ensure the 'data' directory exists, create it if it doesn't
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        
        # Define the file path for schedule.txt
        schedule_txt_path = os.path.join(data_directory, 'schedule.txt')
        
        try:
            with open(schedule_txt_path, "x") as file:
                for i in self.depts:
                    for j in self.arrival:
                        if i == j:
                            pass
                        else:
                            file.write(i + " - TO - " + j + "\n")
                            for k in self.days:
                                file.write(k + "\t\t" + str(self.times[self.t_num]) + "\t\t" + "\t")
                                self.t_num += 1
                                file.write(str(self.times[self.t_num]) + "\n")
                                self.t_num += 1
        except FileExistsError:
            pass

    def read_schedule(self):
        # Define the file path for schedule.txt
        schedule_txt_path = os.path.join(os.getcwd(), 'data', 'schedule.txt')
        
        with open(schedule_txt_path) as file:
            for line in file:
                self.schedule.append(line.strip())

    def save_schedule(self):
        # Define the file path for schedule.txt
        schedule_txt_path = os.path.join(os.getcwd(), 'data', 'schedule.txt')
        
        with open(schedule_txt_path, "w") as file:
            for line in self.schedule:
                file.write(line + "\n")

