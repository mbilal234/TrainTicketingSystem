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

        self.BookButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.ViewButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.CancelButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(3))
        
        self.NameInput.textChanged.connect(lambda: self.CorrectName(self.NameInput, self.submitButton))
        self.cnicInput.textChanged.connect(lambda: self.CorrectCNIC(self.cnicInput, self.submitButton))
        self.DateInput.setMinimumDate(QDate.currentDate())
        self.DateInput.setDate(QDate.currentDate())
        self.DateInput.setMaximumDate(QDate.currentDate().addDays(30))
        self.departureInput.currentTextChanged.connect(lambda: self._updateDestination(self.departureInput, self.destinationInput))
        boxes = [self.NameInput, self.cnicInput, self.dobInput, self.departureInput, self.destinationInput, self.DateInput, self.TypeInput, self.timeInput, self.submitButton]
        details = [self.AvailableCombo, self.SuggestedTime, self.SeatsBox, self.Under2Box, self.Age2t18Box, self.Above60Box, self.BookDetails, self.BerthBox]
        frame = [self.BookingDetailsFrame1, self.FareFrame, self.price, self.amount, self.discount, self.fare, self.bookingID]
        self.submitButton.clicked.connect(lambda: self.BookTicket(boxes, details, frame, 0))
        self.cancelButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))
        self.SeatsBox.valueChanged.connect(lambda: self._update2to18(self.SeatsBox.value(), self.Age2t18Box, self.BookDetails))
        self.Age2t18Box.valueChanged.connect(lambda: self._updateAbove60(self.Age2t18Box.value(), self.Above60Box))
        self.FareFrame.hide()
        global out
        out = [ self.cnicOutput, self.NameOutput, self.FromOutput, self.ToOutput, self.DateOutput, self.DayOutput, self.TimeOutput, self.TypeOutput, self.SeatsOutput]
        self.ViewReservationButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.ViewReservationButton.clicked.connect(lambda: self.ViewReservation(self.NameInput.text(), self.cnicInput.text(), out, self.ViewTicketFrame, self.MessageFrameView))
        L = [self.FareFrame, self.BookingDetailsFrame1, self.AvailableCombo, self.NameInput, self.cnicInput, self.SuggestedTime, self.Above60Box, self.SeatsBox, 
             self.Age2t18Box, self.BookDetails, self.dobInput, self.departureInput, self.destinationInput, self.DateInput, self.TypeInput, self.timeInput]
        self.ViewReservationButton.clicked.connect(lambda: self.SetDefault(L))
        self.MenuButtonBookingTab.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))
        
        self.ViewTicketFrame.hide()
        self.MessageFrameView.hide()
        self.BookingInputBox.textChanged.connect(lambda: self.CorrectBooking(self.BookingInputBox, self.ViewSubmit))
        self.cnicInputBox.textChanged.connect(lambda: self.CorrectCNIC(self.cnicInputBox, self.ViewSubmit))
        self.ViewSubmit.clicked.connect(lambda: self.ViewReservation(self.BookingInputBox.text(), self.cnicInputBox.text(), out, self.ViewTicketFrame, self.MessageFrameView))
        self.MenuButtonViewTab.clicked.connect(lambda: self.ReturnToMenu([self.ViewTicketFrame, self.MessageFrameView], self.BookingInputBox, self.cnicInputBox))
        
        self.CancelTicketFrame.hide()
        self.MessageFrameCancel.hide()
        self.BookingInputCancel.textChanged.connect(lambda: self.CorrectBooking(self.BookingInputCancel, self.CancelSubmit))
        self.cnicInputCancel.textChanged.connect(lambda: self.CorrectCNIC(self.cnicInputCancel, self.CancelSubmit))
        self.CancelSubmit.clicked.connect(self.CancelBooking)
        self.MenuButtonCancelTab.clicked.connect(lambda: self.ReturnToMenu([self.CancelTicketFrame, self.MessageFrameCancel], self.BookingInputCancel, self.cnicInputCancel))
                  
    def CorrectName(self, name, button):
        if not all(x.isalpha() or x.isspace() for x in name.text()) or (name.text() == ""):
            name.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
            button.setEnabled(False)
        else:
            name.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
            button.setEnabled(True)
            
    def CorrectBooking(self, booking, button):
        if not all(x.isdigit() for x in booking.text()) or len(booking.text()) < 3 or (booking.text() == ""):
            booking.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
            button.setEnabled(False)
        else:
            booking.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
            button.setEnabled(True)

    def CorrectCNIC(self, cnic, button):
        if not all(x.isdigit() for x in cnic.text()) or len(cnic.text()) < 13 or (cnic.text() == ""):
            cnic.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
            button.setEnabled(False)
        else:
            cnic.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
            button.setEnabled(True)
    
    def ReturnToMenu(self, frames, name, cnic):
        for frame in frames:
            frame.hide()
        name.setText("")
        cnic.setText("")
        name.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
        cnic.setStyleSheet("color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
        self.tabWidget.setCurrentIndex(0)
        # self.message.setText("")
        
    def _updateDestination(self, depart, dest):
        dest.clear()
        city = depart.currentText()
        if city == "Lahore":
            dest.addItems(("Karachi", "Rawalpindi", "Peshawar", "Quetta"))
        elif city == "Karachi":
            dest.addItems(("Lahore", "Rawalpindi", "Peshawar", "Quetta"))
        elif city == "Rawalpindi":
            dest.addItems(("Lahore", "Karachi", "Peshawar", "Quetta"))
        elif city == "Peshawar":
            dest.addItems(("Lahore", "Karachi", "Rawalpindi", "Quetta"))
        elif city == "Quetta":
            dest.addItems(("Lahore", "Karachi", "Rawalpindi", "Peshawar"))
        
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
        
    def SeatSelection(self, t_type, day, time, dept, dest):
        if time == "":
            pass
        else:
            global train101
            global train100
            with open("../data/Trains.txt","r") as file:
                train100=file.readlines()
                d = 0
                for i in train100:
                    if '"Type": "'+t_type.lower()+'", "Day": "'+day+'", "Time": '+'"'+time+'", '+ '"'+dept.lower()+'": "'+dest.lower()+'"' in i:
                        d=train100.index(i)
                        break
                
                train101=json.loads(train100[d])
            
            if t_type == "Business":
                self.MaxSeats(train101, t_type, "A")
            elif t_type == "Economy":
                self.MaxSeats(train101, t_type)

    def MaxSeats(self, train, typ, berth=""):
        availableSeats = []
        for seat in train.keys():
            if typ == "Business" and berth in seat and train[seat] == True:
                availableSeats.append(seat)
            elif typ == "Economy" and train[seat] == True:
                availableSeats.append(seat)
        self.SeatsBox.setMaximum(len(availableSeats))
        pass
    
    def updateTime(self, day, dept, dest, hr, combobox):
        combobox.clear()
        schedule = []
        diff = timedelta.max
        nearest = ""
        with open("../data/schedule.txt") as op:
            for i in op:
                item = ""
                for j in i:
                    if j != "\n":
                        item += j
                    else:
                        schedule.append(item)
                        break
        for k in schedule:
            if (dept + " - TO - " + dest) in k:
                for l in range(schedule.index(k), schedule.index(k)+7):
                    if schedule[l].startswith(day):
                        s = schedule[l].split("\t")
                        for element in s:
                            if element.isnumeric():
                                combobox.addItem(element[:2]+":"+element[2:])
                                if abs(hr - datetime.strptime(element, "%H%M")) < diff:
                                    nearest = str(datetime.strptime(element, "%H%M"))[11:16]
                                    diff = abs(hr - datetime.strptime(element, "%H%M"))
                                    
        return nearest
    
    def fareCost(self, details):
        ticket_price_econ={"KarachiLahore":3500,"KarachiRawalpindi":3000,"KarachiQuetta":2000,"KarachiPeshawar":4000,
                      "LahoreRawalpindi":1500,"LahoreQuetta":2400,"LahorePeshawar":1800,
                      "RawalpindiQuetta":2800,"RawalpindiPeshawar":1000,
                      "QuettaPeshawar":3600}
        ticket_price_bus={"KarachiLahore":6500,"KarachiRawalpindi":5000,"KarachiQuetta":4500,"KarachiPeshawar":8000,
                      "LahoreRawalpindi":3000,"LahoreQuetta":3400,"LahorePeshawar":3200,
                      "RawalpindiQuetta":5200,"RawalpindiPeshawar":2200,
                      "QuettaPeshawar":7000}
        if details["Type"] == "Economy":
            for i in ticket_price_econ:
                if i == (details["Departure"]+details["Destination"]) or i == (details["Destination"]+details["Departure"]):
                    cost=ticket_price_econ[i]
        elif details["Type"] == "Business":
            for i in ticket_price_bus:
                if i == (details["Departure"]+details["Destination"]) or i == (details["Destination"]+details["Departure"]):
                    cost=ticket_price_bus[i]
        discount = int((0.4*cost*int(details["Kids"])) + (0.2*cost*int(details["Elderly"])))
        orig_cost = int(details["Berth"])*cost + int(details["Seats"])*cost
        fare_cost = orig_cost - discount
        return cost, orig_cost, discount, fare_cost
    
    def FinalSelection(self, details, box, rateframes):
        details["Time"] = box[0].currentText()
        if details["Type"] == "Business":
            details["Berth"] = box[2].value()
            a = int(details["Berth"])
            L = box[-1].currentText()
        else:
            details["Seats"] = box[2].value()
            a = int(details["Seats"])
            L = ""
            
        details["Elderly"] = box[5].value()
        details["Kids"] = box[4].value()
        price = self.fareCost(details)
        details["FareCost"] = price[3] 
        rateframes[0].hide()
        rateframes[1].show()
        rateframes[2].setText("Rs. "+str(price[0]))
        rateframes[3].setText("Rs. "+str(price[1]))
        rateframes[4].setText("Rs. "+str(price[2]))
        rateframes[5].setText("Rs. "+str(price[3]))
        # Booking ID displayed here
        rateframes[6].setText("Booking ID here")
        travelIDs = self.db.get_seats_and_time(details["Departure"], details["Destination"], details["Date"], details["Time"], details["Type"])
        print(travelIDs)
        times = travelIDs['times']
        print(times)
        for i in times:
            print(i)
            print(details["Time"])
            if  details["Time"] in i:
                travelID = travelIDs['times'][i]
        
        self.db.book_ticket(details["BookingID"], details["Name"], travelID, str(details["DOB"]), 0, details["Kids"], details["Elderly"], details["SeatNumber"].split(','))
        
        s = ""
        for i in train101.keys():
            if a == 0:
                break
            elif i.startswith(L) and train101[i]==True:
                train101[i]=False
                s += i + ","
                a-=1
        seats = s[:-1]
        details["SeatNumber"] = seats
        
        try:
            with open('Trains.txt','a') as file:
                for i in train100:
                    if '"Type": "'+details["Type"].lower()+'", "day": "'+details["Day"]+'", "time": '+'"'+(details["Time"])[:2]+(details["Time"])[3:] +'", '+ '"'+details["Departure"].lower()+'": "'+details["Destination"].lower()+'"' in i:
                        train100.remove(i)

            with open('Trains.txt','w') as file:
                for i in train100:
                    i=json.loads(i)
                    file.write(json.dumps(i))
                    file.write("\n")
                file.write(json.dumps(train101))
        except:
            pass
        
        with open('TrainReservation.csv', mode='a') as file:
            keys = ["BookingID", "Name", "DOB", "Departure", "Destination", "Date", "Day", 
                    "Time", "Type", "Seats", "Berth", "FareCost", "Elderly", "Kids", "SeatNumber"]
            w = csv.DictWriter(file, fieldnames=keys)
            w.writerow(details)
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
        t = datetime.strptime(preferredtime.strftime('%H:%M'),'%H:%M')
        
        for func in inputbox:
            func.setEnabled(False)
        
        suggestedtime = self.updateTime(day, dept, dest, t, moredetails[0])
        moredetails[1].setText(suggestedtime)
        
        for i in moredetails:    
            if type(i) is not list:
                i.setEnabled(True)
        if t_type == "Economy":
            moredetails[-1].setEnabled(False)
            
        self.SeatSelection(t_type, day, moredetails[0].currentText()[:2]+moredetails[0].currentText()[3:], dept, dest)
        moredetails[0].currentTextChanged.connect(lambda: self.SeatSelection(t_type, day, moredetails[0].currentText()[:2]+moredetails[0].currentText()[3:], dept, dest))
        moredetails[-1].currentTextChanged.connect(lambda: self.MaxSeats(train101, t_type, moredetails[-1].currentText()))
        
        reservation = {"BookingID": cnic, "Name": name, "DOB": dob, "Departure": dept, "Destination": dest, "Date": date, "Day": day, 
                       "Time": '', "Type": t_type, "Seats": '0', "Berth": '0', "FareCost": '0', "Elderly": '', "Kids": '', "SeatNumber": ''}
        if signal == 1:
            moredetails[-2].clicked.connect(lambda: self.RemoveBooking(moredetails[-3]))
        moredetails[-2].clicked.connect(lambda: self.FinalSelection(reservation, moredetails, frame))
        
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
        
    def UpdateReservation(self):
        name = self.NameInputUpdate.text()
        cnic = self.cnicInputUpdate.text()
        row = self.ReadFile(name, cnic)
        if row == []:
            pass
        else:
            self.dobInputUpdate.setDate(QDate.fromString(row[2], "yyyy-MM-dd"))
            in_box = [self.NameInputUpdate, self.cnicInputUpdate, self.dobInputUpdate, self.departureInputUpdate, self.destinationInputUpdate, self.DateInputUpdate, self.TypeInputUpdate, self.timeInputUpdate, self.UpdateRes]
            details_out = [self.AvailableComboUpdate, self.SuggestedTimeUpdate, self.SeatsBoxUpdate, self.Under2BoxUpdate, self.Age2t18BoxUpdate, self.Above60BoxUpdate, row, self.UpdateDetails, self.BerthBoxUpdate]
            frame = [self.UpdateBookingFrame, self.FareFrameU, self.priceU, self.amountUpdate, self.discountUpdate, self.fareUpdate]
            self.UpdateBookingFrame.show()
            self.departureInputUpdate.setCurrentText(row[3])
            self.destinationInputUpdate.setCurrentText(row[4])
            self.DateInputUpdate.setDate(QDate.fromString(row[5], "yyyy-MM-dd"))
            self.timeInputUpdate.setTime(QTime.fromString(row[7], "hh:mm"))
            self.TypeInputUpdate.setCurrentText(row[8])
            if int(row[9]) > 0:
                self.SeatsBoxUpdate.setValue(int(row[9]))
            else:
                self.SeatsBoxUpdate.setValue(int(row[10]))
            self.Above60BoxUpdate.setValue(int(row[12]))
            self.Age2t18BoxUpdate.setValue(int(row[13]))
            self.UpdateRes.clicked.connect(lambda: self.BookTicket(in_box, details_out, frame, 1))
        
    def ReadFile(self, name, cnic):
        with open('TrainReservation.csv', 'r') as file:
            w = csv.reader(file)
            for row in w:
                if name in row and cnic in row:
                    return row
            else:
                return []
        pass
        
    def ViewReservation(self, name, cnic, outputs, frame, messageFrame):
        details = self.db.view_booking(int(name),cnic)
        row = self.ReadFile(name, cnic)
        if row == []:
            messageFrame.show()
        else:
            outputs[0].setText(details['cnic'])
            outputs[1].setText(details['name'])
            outputs[2].setText(details['departure'])
            outputs[3].setText(details['destination'])
            outputs[4].setText(details['dateOfBirth'])
            outputs[5].setText(details['numberOfSeats'])
            outputs[6].setText(details['travelId'])
            outputs[7].setText(details['timestamp'])
            outputs[8].setText(details['cost'])
    
    def RemoveBooking(self,  details):
        L = []
        with open("Trains.txt") as op:
            for i in op:
                L.append(i)
        for i,k in enumerate(L):
            if '"Type": "'+details[8].lower()+'", "day": "'+details[6]+'", "time": '+'"'+(details[7])[:2]+(details[7])[3:] +'", '+ '"'+details[3].lower()+'": "'+details[4].lower()+'"' in k:
                d = json.loads(k)
                for key in d:
                    if key in details[-1] and d[key] == False:
                        d[key] = True
                e = json.dumps(d)
                L[i] = e
            else:
                L[i] = k
        with open("Trains.txt", "w") as op:
            for i in L:
                op.write(i)
                
        with open('TrainReservation.csv','r') as file:
            customer_info = DictReader(file)
            lis=[{'BookingID': '', ' Name': '', 'DOB': '', ' Departure': '', ' Destination': '', ' Date': '', ' Day': '', ' Time': '', ' Type': '', ' Seats': '', ' Berth': '', ' FareCost': '', ' Elderly': '', ' Kids': '', ' SeatNumber': ''}]
            for i in customer_info:
                lis.append(i)
                for j in lis:
                    if details[0] in j.values() and details[1] in j.values():
                        lis.remove(j)
        keys=lis[0].keys()
        with open('TrainReservation.csv','w') as file:
            dict_writer=csv.DictWriter(file,keys)
            dict_writer.writeheader()
            dict_writer.writerows(lis)
    
    def CancelBooking(self):
        name = self.BookingInputCancel.text()
        cnic = self.cnicInputCancel.text()
        try:
            self.db.cancel_booking(name,cnic)
        except:
            print("Not removed!!!")
        row = self.ReadFile(name, cnic)
        outCancel = [self.cnicOutputCancel, self.NameOutputCancel, self.FromOutputCancel, self.ToOutputCancel, 
                     self.DateOutputCancel, self.DayOutputCancel, self.TimeOutputCancel, 
                     self.TypeOutputCancel, self.SeatsOutputCancel]
        
        if row == []:
            pass
        else:
            self.ViewReservation(name, cnic, outCancel, self.CancelTicketFrame, self.MessageFrameCancel)
            self.message.setText("Your Booking has been successfully cancelled! A refund of 50% has been transferred to your account.")
            self.RemoveBooking(row)
        
# schedule_maker()
# trains_maker()
try:
    f = open("TrainReservation.txt", "x")
except:
    pass
else:
    CustomerInformation.CustomerInformation()