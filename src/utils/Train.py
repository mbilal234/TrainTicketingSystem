import json
import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import *
import calendar
import csv
from csv import DictReader
from datetime import datetime, timedelta
import os

class Train:
    """
    The Train class represents a train with specific attributes such as train ID, type, day, time, departure,
    arrival, and available seats.

    Attributes:
    - train_id (str): The unique identifier for the train.
    - train_type (str): The type or category of the train.
    - day (str): The day of the week when the train operates.
    - time (str): The departure time of the train.
    - departure (str): The departure station or location.
    - arrival (str): The arrival station or location.
    - seats (dict): A dictionary representing the available seats on the train.

    Methods:
    - to_json(): Converts the Train object to a JSON-compatible dictionary for serialization.

    Example Usage:
    train = Train("T123", "Express", "MON", "08:00 AM", "Karachi", "Lahore", {"Economy": 50, "Business": 20})
    train_data = train.to_json()  # Convert the Train object to a JSON-compatible dictionary.
    """
    def __init__(self, train_id, train_type, day, time, departure, arrival, seats):
        """
        Initializes a Train object with the provided attributes.

        Parameters:
        - train_id (str): The unique identifier for the train.
        - train_type (str): The type or category of the train.
        - day (str): The day of the week when the train operates.
        - time (str): The departure time of the train.
        - departure (str): The departure station or location.
        - arrival (str): The arrival station or location.
        - seats (dict): A dictionary representing the available seats on the train.

        Returns:
        None
        """
        self.train_id = train_id
        self.train_type = train_type
        self.day = day
        self.time = time
        self.departure = departure
        self.arrival = arrival
        self.seats = seats

    def to_json(self):
        """
        Converts the Train object to a JSON-compatible dictionary for serialization.

        Returns:
        dict: A dictionary representation of the Train object.
        """
        return {
            "TrainID": self.train_id,
            "Type": self.train_type,
            "Day": self.day,
            "Time": self.time,
            self.departure: self.arrival,
            **self.seats
        }
