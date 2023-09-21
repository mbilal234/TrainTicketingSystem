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
    def __init__(self, train_id, train_type, day, time, departure, arrival, seats):
        self.train_id = train_id
        self.train_type = train_type
        self.day = day
        self.time = time
        self.departure = departure
        self.arrival = arrival
        self.seats = seats

    def to_json(self):
        return {
            "TrainID": self.train_id,
            "Type": self.train_type,
            "Day": self.day,
            "Time": self.time,
            self.departure: self.arrival,
            **self.seats
        }
