# Import necessary modules and classes
from utils import  GUI
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
import sys
import pymongo
from dotenv import load_dotenv
import os

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
        Non

    Returns:
        None
    """
        
    load_dotenv()

    my_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = my_client["test_trs"]
    print(db)

    # Create a QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Create the main GUI window
    window = GUI.MainWindow()

    # Show the main window
    window.show()

    # Run the QApplication event loop
    sys.exit(app.exec())

# Entry point of the program
if __name__ == "__main__":
    main()
