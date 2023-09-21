import os
import pandas as pd

def CustomerInformation():
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

