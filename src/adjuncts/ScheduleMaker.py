import os

class ScheduleMaker:
    """
    The ScheduleMaker class is designed to generate, read, and save schedules for train departures and arrivals.

    It includes methods for generating a schedule, reading an existing schedule from a file, and saving the
    schedule to a file.

    Attributes:
    - schedule (list): A list to store the schedule information as strings.
    - depts (list): A list of departure locations.
    - arrival (list): A list of arrival locations.
    - days (list): A list of days of the week.
    - times (list): A list of departure and arrival times.
    - t_num (int): An internal variable to keep track of the time index during schedule generation.

    Methods:
    - generate_schedule(): Generates a schedule and writes it to a 'schedule.txt' file.
    - read_schedule(): Reads a schedule from the 'schedule.txt' file and stores it in the 'schedule' attribute.
    - save_schedule(): Saves the schedule stored in the 'schedule' attribute to the 'schedule.txt' file.

    Example Usage:
    schedule_maker = ScheduleMaker()  # Create an instance of the ScheduleMaker class.
    schedule_maker.generate_schedule()  # Generate and save a schedule.
    schedule_maker.read_schedule()  # Read the saved schedule from the file.
    schedule_maker.save_schedule()  # Save any modifications to the schedule back to the file.
    """
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
        """
        Generates a train schedule and writes it to a 'schedule.txt' file.

        The generated schedule includes information about departures and arrivals between different locations,
        including days of the week and corresponding departure and arrival times.

        Parameters:
        None

        Returns:
        None
        """
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
        """
        Reads a train schedule from the 'schedule.txt' file and stores it in the 'schedule' attribute.

        Parameters:
        None

        Returns:
        None
        """
        # Define the file path for schedule.txt
        schedule_txt_path = os.path.join(os.getcwd(), 'data', 'schedule.txt')
        
        with open(schedule_txt_path) as file:
            for line in file:
                self.schedule.append(line.strip())

    def save_schedule(self):
        """
        Saves the schedule stored in the 'schedule' attribute to the 'schedule.txt' file.

        Parameters:
        None

        Returns:
        None
        """
        # Define the file path for schedule.txt
        schedule_txt_path = os.path.join(os.getcwd(), 'data', 'schedule.txt')
        
        with open(schedule_txt_path, "w") as file:
            for line in self.schedule:
                file.write(line + "\n")

