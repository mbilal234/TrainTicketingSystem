# Import necessary modules and classes
from adjuncts import CustomerInformation, GUI, ScheduleMaker, Train, TrainsMaker
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import *
import sys

def main():
    """
    The main function for running the Train Reservation System.

    This function performs the following tasks:
    1. Generates a schedule using ScheduleMaker.
    2. Reads and modifies the schedule list as needed.
    3. Saves the schedule to a file.
    4. Generates train objects using TrainsMaker.
    5. Saves the train objects to a file.
    6. Creates a QApplication for the GUI.
    7. Initializes and shows the main GUI window.
    8. Runs the QApplication event loop.

    Args:
        None

    Returns:
        None
    """
    
    # Create an instance of ScheduleMaker
    schedule_maker = ScheduleMaker.ScheduleMaker()

    # Generate a schedule
    schedule_maker.generate_schedule()

    # Read the schedule from file
    schedule_maker.read_schedule()

    # Modify the schedule list if needed
    # (Add any necessary schedule modifications here)

    # Save the modified schedule to a file
    schedule_maker.save_schedule()

    # Create an instance of TrainsMaker
    trains_maker = TrainsMaker.TrainsMaker()

    # Generate train objects
    trains = trains_maker.generate_train_objects()

    # Save the train objects to a file
    trains_maker.save_trains_to_file(trains)

    # Try to create a file for customer information (if it doesn't already exist)
    try:
        f = open("TrainReservation.txt", "x")
    except FileExistsError:
        pass
    else:
        # If the file is created, initialize the CustomerInformation class
        CustomerInformation.CustomerInformation()

    # Create a QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Create the main GUI window
    window = GUI.MainWindow()

    # Show the main window
    window.show()

    # Run the QApplication event loop
    app.exec_()

# Entry point of the program
if __name__ == "__main__":
    main()
