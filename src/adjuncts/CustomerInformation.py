import os
import pandas as pd

def CustomerInformation():
    """
    This function manages customer information for a train reservation system.

    It performs the following tasks:
    1. Retrieves the current working directory.
    2. Defines the data directory path (assuming it's at the same level as 'src').
    3. Ensures that the 'data' directory exists and creates it if it doesn't.
    4. Defines file paths for 'TrainReservation.txt' and 'TrainReservation.csv'.
    5. Writes a header to the 'TrainReservation.txt' file if it doesn't already exist.
    6. Reads the 'TrainReservation.txt' file and saves its content as 'TrainReservation.csv'.

    The function is designed to initialize and manage data files for train reservation information.

    Parameters:
    None

    Returns:
    None

    Example Usage:
    CustomerInformation()  # Calls the function to manage customer information.
    """
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Define the data directory path (assuming it's at the same level as 'src')
    data_directory = os.path.join(current_directory, 'data')
    
    # Ensure the 'data' directory exists, create it if it doesn't
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    
    # Define the file paths
    train_reservation_txt_path = os.path.join(data_directory, 'TrainReservation.txt')
    train_reservation_csv_path = os.path.join(data_directory, 'TrainReservation.csv')
    
    # Write the header to the TrainReservation.txt file
    with open(train_reservation_txt_path, "a") as op:
        op.write("BookingID, Name, DOB, Departure, Destination, Date, Day, Time, Type, Seats, Berth, FareCost, Elderly, Kids, SeatNumber\n")
    
    # Read the TrainReservation.txt file and save it as TrainReservation.csv
    read_file = pd.read_csv(train_reservation_txt_path)
    read_file.to_csv(train_reservation_csv_path, index=None)
