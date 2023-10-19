# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 14:18:25 2022

@author: M. Ashhub Ali
"""

import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import *
import calendar
import csv
from csv import DictReader
from datetime import datetime, timedelta
import os
import json
from adjuncts import ScheduleMaker, TrainsMaker, CustomerInformation
from db import DatabaseConnection, DatabaseFunctions


directory = os.getcwd()


class MainWindow(QtWidgets.QMainWindow):
    """
    The MainWindow class represents the main window of the Train Reservation System application.

    Attributes:
    - directory (str): The current working directory.

    Methods:
    - CorrectName(name, button): Validates and corrects the name input field.
    - CorrectCNIC(cnic, button): Validates and corrects the CNIC input field.
    - ReturnToMenu(frame, name, cnic): Hides a given frame and resets input fields, enabling navigation to the main menu.
    - _updateDestination(depart, dest): Updates the destination based on the selected departure city.
    - _update2to18(val1, box1, button): Updates available seats for passengers between 2 and 18 years old.
    - _updateAbove60(val2, box2): Updates available seats for passengers above 60 years old.
    - SeatSelection(t_type, day, time, dept, dest): Selects available seats based on train type, day, time, departure, and destination.
    - MaxSeats(train, typ, berth=""): Calculates the maximum available seats based on the train type and berth.
    - updateTime(day, dept, dest, hr, combobox): Updates the available time slots based on the selected day, departure, and destination.
    - fareCost(details): Calculates fare cost and discounts based on passenger details and train type.
    - FinalSelection(details, box, rateframes): Finalizes the ticket booking with fare details and seat allocation.
    - BookTicket(inputbox, moredetails, frame, signal): Handles the booking process, input validation, and seat selection.
    - SetDefault(L): Resets input fields and enables passenger details input for a new booking.
    - UpdateReservation(): Handles updating an existing reservation.
    - ReadFile(name, cnic): Reads passenger information from the CSV file.
    - ViewReservation(name, cnic, outputs, frame): Views passenger reservation details.
    - RemoveBooking(details): Removes a passenger's booking, releasing the booked seats.
    - CancelBooking(): Handles the cancellation of a booking and refunds.

    Example Usage:
    - Create an instance of the MainWindow class to run the Train Reservation System application.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(directory+r"\\train.ui", self)
        self.setWindowTitle("Train Reservation System")
        self.setWindowIcon(QtGui.QIcon("assets\\train.png"))
        self.db = DatabaseFunctions.DatabaseFunction()

        self.BookButton.clicked.connect(
            lambda: self.tabWidget.setCurrentIndex(1))
        self.ViewButton.clicked.connect(
            lambda: self.tabWidget.setCurrentIndex(2))
        self.CancelButton.clicked.connect(
            lambda: self.tabWidget.setCurrentIndex(3))

        self.NameInput.textChanged.connect(
            lambda: self.CorrectName(self.NameInput, self.submitButton))
        self.cnicInput.textChanged.connect(
            lambda: self.CorrectCNIC(self.cnicInput, self.submitButton))
        self.DateInput.setMinimumDate(QDate.currentDate())
        self.DateInput.setDate(QDate.currentDate())
        self.DateInput.setMaximumDate(QDate.currentDate().addDays(30))
        self.departureInput.currentTextChanged.connect(
            lambda: self._updateDestination(self.departureInput, self.destinationInput))
        boxes = [self.NameInput, self.cnicInput, self.dobInput, self.departureInput,
                 self.destinationInput, self.DateInput, self.TypeInput, self.timeInput, self.submitButton]
        details = [self.AvailableCombo, self.SuggestedTime, self.SeatsBox, self.Under2Box,
                   self.Age2t18Box, self.Above60Box, self.BookDetails, self.BerthBox]
        frame = [self.BookingDetailsFrame1, self.FareFrame, self.price,
                 self.amount, self.discount, self.fare, self.bookingID]

        self.submitButton.clicked.connect(
            lambda: self.BookTicket(boxes, details, frame, 0))
        self.cancelButton.clicked.connect(
            lambda: self.tabWidget.setCurrentIndex(0))
        self.SeatsBox.valueChanged.connect(lambda: self._update2to18(
            self.SeatsBox.value(), self.Age2t18Box, self.BookDetails))
        self.Age2t18Box.valueChanged.connect(
            lambda: self._updateAbove60(self.Age2t18Box.value(), self.Above60Box))
        self.FareFrame.hide()
        global out
        out = [self.cnicOutput, self.NameOutput, self.FromOutput, self.ToOutput,
               self.DateOutput, self.DayOutput, self.TimeOutput, self.TypeOutput, self.SeatsOutput]
        self.ViewReservationButton.clicked.connect(
            lambda: self.tabWidget.setCurrentIndex(2))

        L = [self.FareFrame, self.BookingDetailsFrame1, self.AvailableCombo, self.NameInput, self.cnicInput, self.SuggestedTime, self.Above60Box, self.SeatsBox,
             self.Age2t18Box, self.BookDetails, self.dobInput, self.departureInput, self.destinationInput, self.DateInput, self.TypeInput, self.timeInput]
        self.ViewReservationButton.clicked.connect(lambda: self.SetDefault(L))
        self.MenuButtonBookingTab.clicked.connect(
            lambda: self.tabWidget.setCurrentIndex(0))

        self.ViewTicketFrame.hide()
        self.MessageFrameView.hide()
        self.BookingInputBox.textChanged.connect(
            lambda: self.CorrectBooking(self.BookingInputBox, self.ViewSubmit))
        self.cnicInputBox.textChanged.connect(
            lambda: self.CorrectCNIC(self.cnicInputBox, self.ViewSubmit))
        self.ViewSubmit.clicked.connect(lambda: self.ViewReservation(self.BookingInputBox.text(
        ), self.cnicInputBox.text(), out, self.ViewTicketFrame, self.MessageFrameView))
        self.MenuButtonViewTab.clicked.connect(lambda: self.ReturnToMenu(
            [self.ViewTicketFrame, self.MessageFrameView], self.BookingInputBox, self.cnicInputBox))

        self.CancelTicketFrame.hide()
        self.MessageFrameCancel.hide()
        self.BookingInputCancel.textChanged.connect(
            lambda: self.CorrectBooking(self.BookingInputCancel, self.CancelSubmit))
        self.cnicInputCancel.textChanged.connect(
            lambda: self.CorrectCNIC(self.cnicInputCancel, self.CancelSubmit))
        self.CancelSubmit.clicked.connect(self.CancelBooking)
        self.MenuButtonCancelTab.clicked.connect(lambda: self.ReturnToMenu(
            [self.CancelTicketFrame, self.MessageFrameCancel], self.BookingInputCancel, self.cnicInputCancel))

    def CorrectName(self, name, button):
        if not all(x.isalpha() or x.isspace() for x in name.text()) or (name.text() == ""):
            name.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
            button.setEnabled(False)
        else:
            name.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
            button.setEnabled(True)

    def CorrectBooking(self, booking, button):
        if not all(x.isdigit() for x in booking.text()) or len(booking.text()) not in [4, 5] or (booking.text() == ""):
            booking.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
            button.setEnabled(False)
        else:
            booking.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
            button.setEnabled(True)

    def CorrectCNIC(self, cnic, button):
        if not all(x.isdigit() for x in cnic.text()) or len(cnic.text()) < 13 or (cnic.text() == ""):
            cnic.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
            button.setEnabled(False)
        else:
            cnic.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
            button.setEnabled(True)

    def ReturnToMenu(self, frames, name, cnic):
        for frame in frames:
            frame.hide()
        name.setText("")
        cnic.setText("")
        name.setStyleSheet(
            "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
        cnic.setStyleSheet(
            "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
        self.tabWidget.setCurrentIndex(0)
        # self.message.setText("")

    def _updateDestination(self, depart, dest):
        dest.clear()
        city = depart.currentText()
        for destination in ["Lahore", "Karachi", "Rawalpindi", "Peshawar", "Quetta"]:
            if destination != city:
                dest.addItem(destination)

    def _update2to18(self, val1, box1, button):
        global totalseats
        totalseats = val1
        box1.setMaximum(totalseats)
        if val1 == 0:
            button.setEnabled(False)
        else:
            button.setEnabled(True)

    def _updateAbove60(self, val2, box2):
        global age2To18
        age2To18 = val2
        box2.setMaximum(totalseats - age2To18)

    def SeatSelection(self, t_type, travel_id):
        print("Seat Selection:", t_type, travel_id)
        if travel_id and t_type:
            if t_type == "Business":
                self.MaxSeats(travel_id, t_type, "A")
            elif t_type == "Economy":
                self.MaxSeats(travel_id, t_type)

    def MaxSeats(self, travel_id, typ, berth=""):
        print("Seat Max:", typ, travel_id)
        if typ == "Business" and berth in ["A", "B", "C", "D", "E", "F"]:
            self.SeatsBox.setMaximum(
                len(self.db.get_business_seats(travel_id, berth)['seats']))
        elif typ == "Economy":
            self.SeatsBox.setMaximum(
                len(self.db.get_economy_seats(travel_id)['seats']))
        else:
            self.SeatsBox.setMaximum(0)

    def updateTime(self, times, combobox):
        combobox.clear()
        for i in times.keys():
            combobox.addItem(i.split(' ')[1][:-3])

    def fareCost(self, details):
        cost = self.db.get_fare(
            details["Departure"], details["Destination"], details["Type"].lower())

        discount = int(
            (0.4*cost*int(details["Kids"])) + (0.2*cost*int(details["Elderly"])))
        orig_cost = int(details["Seats"])*cost
        fare_cost = orig_cost - discount
        return cost, orig_cost, discount, fare_cost

    def FinalSelection(self, details, box, rateframes):
        details["Time"] = box[0].currentText()
        if details["Type"] == "Business":
            details["Berth"] = box[-1].currentText()
            details["Seats"] = box[2].value()
        else:
            details["Seats"] = box[2].value()

        details["Elderly"] = box[5].value()
        details["Kids"] = box[4].value()
        price = self.fareCost(details)
        details["FareCost"] = price[3]

        travelIDs = self.db.get_seats_and_time(
            details["Departure"], details["Destination"], details["Date"], details["Time"], details["Type"].lower())
        print(travelIDs)
        times = travelIDs['times']
        print(times)
        for i in times:
            print(i)
            print(details["Time"])
            if details["Time"] in i:
                travelID = travelIDs['times'][i]

        id = self.db.book_ticket(details["CNIC"], details["Name"], travelID, details["Type"].lower(
        ), details["Berth"], str(details["DOB"]), 0, details["Kids"], details["Elderly"], int(details["Seats"]))

        rateframes[0].hide()
        rateframes[1].show()
        rateframes[2].setText("Rs. "+str(price[0]))
        rateframes[3].setText("Rs. "+str(price[1]))
        rateframes[4].setText("Rs. "+str(price[2]))
        rateframes[5].setText("Rs. "+str(price[3]))
        rateframes[6].setText(str(id))

        self.ViewReservationButton.clicked.connect(lambda: self.ViewReservation(
            id, self.cnicInput.text(), out, self.ViewTicketFrame, self.MessageFrameView))
        return None

    def BookTicket(self, inputbox, moredetails, frame, signal):
        name = inputbox[0].text()
        cnic = inputbox[1].text()
        print(name, cnic)
        tempdob = inputbox[2].date()
        dob = tempdob.toPyDate()
        dept = inputbox[3].currentText()
        dest = inputbox[4].currentText()
        tempdate = inputbox[5].date()
        t_type = inputbox[6].currentText()
        date = tempdate.toPyDate()
        day = ((calendar.day_name[date.weekday()]).upper())[:3]
        temptime = inputbox[7].time()
        preferredtime = temptime.toPyTime()
        t = preferredtime.strftime('%H:%M')

        if t_type == "Business":
            time_and_seats = self.db.get_seats_and_time(
                dept, dest, date, t, "business")
        elif t_type == "Economy":
            time_and_seats = self.db.get_seats_and_time(
                dept, dest, date, t, "economy")

        if type(time_and_seats) is str:
            return None

        for func in inputbox:
            func.setEnabled(False)

        suggestedtime = time_and_seats['suggested'].split(' ')[1][:-3]
        moredetails[1].setText(suggestedtime)
        self.updateTime(time_and_seats['times'], moredetails[0])

        for i in moredetails:
            if type(i) is not list:
                i.setEnabled(True)
            moredetails[-2].setEnabled(False)
        if t_type == "Economy":
            moredetails[-1].setEnabled(False)

        print("Book Ticket:", t_type)

        self.SeatSelection(
            t_type, time_and_seats['times'][time_and_seats['suggested']])
        moredetails[0].currentTextChanged.connect(lambda: self.SeatSelection(t_type, time_and_seats['times'][time_and_seats['suggested'].split(
            ' ')[0] + ' ' + (moredetails[0].currentText() + ':00' if moredetails[0].currentText() else time_and_seats['suggested'].split(' ')[1])]))
        moredetails[-1].currentTextChanged.connect(lambda: self.MaxSeats(
            time_and_seats['times'][time_and_seats['suggested'].split(
                ' ')[0] + ' ' + (moredetails[0].currentText() + ':00' if moredetails[0].currentText() else time_and_seats['suggested'].split(' ')[1])], t_type, moredetails[-1].currentText()))

        reservation = {"CNIC": cnic, "Name": name, "DOB": dob, "Departure": dept, "Destination": dest, "Date": date, "Day": day,
                       "Time": '', "Type": t_type, "Seats": 0, "Berth": 0, "FareCost": 0, "Elderly": 0, "Kids": 0}

        moredetails[-2].clicked.connect(
            lambda: self.FinalSelection(reservation, moredetails, frame))

    def SetDefault(self, L):
        L[0].hide()
        L[1].show()
        L[2].clear()
        L[3].clear()
        L[4].clear()
        L[3].setStyleSheet("border: 1px solid black;")
        L[4].setStyleSheet("border: 1px solid black;")
        L[5].setText("00:00")
        L[6].setValue(0)
        L[7].setValue(0)
        L[8].setValue(0)
        for i in L:
            if i == 9:
                i.setEnabled(False)
            else:
                i.setEnabled(True)

    def ViewReservation(self, bookingId, cnic, outputs, frame, messageFrame):
        details = self.db.view_booking(int(bookingId), cnic)
        print("The booking details are", details)
        if details == None:
            messageFrame.show()
        else:
            frame.show()
            outputs[0].setText(cnic)
            outputs[1].setText(details['name'])
            outputs[2].setText(details['departure'])
            outputs[3].setText(details['destination'])
            outputs[4].setText(details['date'])
            outputs[5].setText(str(details['numberOfSeats']))
            outputs[6].setText(str(details['time']))
            outputs[7].setText(details['class'])
            outputs[8].setText(str(','.join(details['seats'])))

    def RemoveBooking(self,  details):
        self.db.cancel_booking(details['bookingId'], details['cnic'])

    def CancelBooking(self):
        bookingId = self.BookingInputCancel.text()
        cnic = self.cnicInputCancel.text()
        details = self.db.view_booking(int(bookingId), cnic)
        outCancel = [self.cnicOutputCancel, self.NameOutputCancel, self.FromOutputCancel, self.ToOutputCancel,
                     self.DateOutputCancel, self.DayOutputCancel, self.TimeOutputCancel,
                     self.TypeOutputCancel, self.SeatsOutputCancel]

        if details and len(details) > 0:
            self.ViewReservation(bookingId, cnic, outCancel,
                                 self.CancelTicketFrame, self.MessageFrameCancel)
            # self.message.setText("Your Booking has been successfully cancelled! A refund of 50% has been transferred to your account.")
            self.RemoveBooking(details)
