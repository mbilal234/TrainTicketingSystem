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

directory = os.getcwd()

def trains_maker():
    true = True
    depts = ["karachi", "lahore", "rawalpindi", "quetta", "peshawar"]
    arrival = ["karachi", "lahore", "rawalpindi", "quetta", "peshawar"]
    days = ["MON", "MON", "TUE", "TUE", "WED", "WED", "THU", "THU", "FRI", "FRI", "SAT", "SAT", "SUN", "SUN", ]
    types = ["economy", "business"]
    id = 1001
    times = ["0800", "1600", "0900", "1700", "1000", "1800", "1100", "1900", "1200", "2000", "1300", "2100", "1400",
             "2200", "1500", "2300", "0830", "1630", "0930", "1730", "1030", "1830", "1130", "1930", "1230", "2030",
             "1330", "2130", "1430", "2230", "1530", "2330"] * 100
    keys = []
    values = []
    t_num = 0

    try:
        f = open("Trains.txt", "x")
    except:
        pass
    else:
        for i in depts:
            for j in arrival:
                if i == j:
                    pass
                else:
                    for k in days:
                        for l in types:
                            if l == "economy":
                                dc = '{"Train' + str(id - 1000) + '": "' + str(
                                    id) + '", "Type": "' + l + '", "day": ' + '"' + k + '"' + ', "time": ' + '"' + \
                                     times[
                                         t_num] + '"' + ', "' + i + '"' + ': ' + '"' + j + '", "1": true, "2": true, "3": true, "4": true, "5": true, "6": true, "7": true, "8": true, "9": true, "10": true, "11": true, "12": true, "13": true, "14": true, "15": true, "16": true, "17": true, "18": true, "19": true, "20": true, "21": true, "22": true, "23": true, "24": true,"25": true, "26": true, "27": true, "28": true, "29": true, "30": true}'

                                with open("Trains.txt", "a") as op:
                                    op.write(dc + "\n")
                            elif l == "business":
                                dc = '{"Train' + str(id - 1000) + '": "' + str(
                                    id) + '", "Type": "' + l + '", "day": ' + '"' + k + '"' + ', "time": ' + '"' + \
                                     times[
                                         t_num] + '"' + ', "' + i + '"' + ': ' + '"' + j + '", "A1": true, "A2": true, "A3": true, "A4": true, "A5": true, "A6": true, "B1": true, "B2": true, "B3": true, "B4": true, "B5": true, "B6": true, "C1": true, "C2": true, "C3": true, "C4": true, "C5": true, "C6": true, "D1": true, "D2": true, "D3": true, "D4": true, "D5": true, "D6": true, "E1": true, "E2": true, "E3": true, "E4": true, "E5": true, "E6": true}'

                                id += 1
                                with open("Trains.txt", "a") as op:
                                    op.write(dc + "\n")
                                    t_num += 1
def schedule_maker():
    global schedule
    schedule = []
    depts = ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Peshawar"]
    arrival = ["Karachi", "Lahore", "Rawalpindi", "Quetta", "Peshawar"]
    days = ["MON", "TUE", "WED","THU", "FRI", "SAT", "SUN"]
    times = ["0800", "1600", "0900", "1700", "1000", "1800", "1100", "1900", "1200", "2000", "1300", "2100", "1400", "2200", "1500", "2300", "0830", "1630", "0930", "1730", "1030", "1830", "1130", "1930", "1230", "2030", "1330", "2130", "1430", "2230", "1530", "2330"]*100
    t_num = 0


    try:
        f = open("schedule.txt", "x")
    except:
        pass
    else:
        with open("schedule.txt", "a") as op:
            for i in depts:
                for j in arrival:
                    if i == j:
                        pass
                    else:
                        op.write(i + " - TO - " + j +"\n")
                        for k in days:
                            op.write(k + "\t\t" + str(times[t_num]) + "\t\t" + "\t")
                            t_num += 1
                            op.write(str(times[t_num]) + "\n")
                            t_num += 1
    with open("schedule.txt") as op:
        for i in op:
            item = ""
            for j in i:
                if j != "\n":
                    item += j
                else:
                    schedule.append(item)
                    break

def customer_information():
    import pandas as pd
    directory = os.getcwd()
    with open("TrainReservation.txt", "a") as op:
        op.write(
            "BookingID, Name, DOB, Departure, Destination, Date, Day, Time, Type, Seats, Berth, FareCost, Elderly, Kids, SeatNumber" + "\n")
    read_file = pd.read_csv(directory + r'\TrainReservation.txt')
    read_file.to_csv(directory + r'\TrainReservation.csv', index=None)
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(directory+r"\\train.ui", self)
        self.setWindowTitle("Train Reservation System")
        self.BookButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.ViewButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.UpdateButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(3))
        self.CancelButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(4))
        
        self.NameInput.textChanged.connect(lambda: self.CorrectName(self.NameInput, self.submitButton))
        self.cnicInput.textChanged.connect(lambda: self.CorrectCNIC(self.cnicInput, self.submitButton))
        self.departureInput.currentTextChanged.connect(lambda: self._updateDestination(self.departureInput, self.destinationInput))
        boxes = [self.NameInput, self.cnicInput, self.dobInput, self.departureInput, self.destinationInput, self.DateInput, self.TypeInput, self.timeInput, self.submitButton]
        details = [self.AvailableCombo, self.SuggestedTime, self.SeatsBox, self.Under2Box, self.Age2t18Box, self.Above60Box, self.BookDetails, self.BerthBox]
        frame = [self.BookingDetailsFrame1, self.FareFrame, self.price, self.amount, self.discount, self.fare]
        self.submitButton.clicked.connect(lambda: self.BookTicket(boxes, details, frame, 0))
        self.cancelButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))
        self.SeatsBox.valueChanged.connect(lambda: self._update2to18(self.SeatsBox.value(), self.Age2t18Box, self.BookDetails))
        self.Age2t18Box.valueChanged.connect(lambda: self._updateAbove60(self.Age2t18Box.value(), self.Above60Box))
        self.FareFrame.hide()
        global out
        out = [ self.cnicOutput, self.NameOutput, self.FromOutput, self.ToOutput, self.DateOutput, self.DayOutput, self.TimeOutput, self.TypeOutput, self.SeatsOutput]
        self.ViewReservationButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.ViewReservationButton.clicked.connect(lambda: self.ViewReservation(self.NameInput.text(), self.cnicInput.text(), out, self.ViewTicketFrame))
        L = [self.FareFrame, self.BookingDetailsFrame1, self.AvailableCombo, self.NameInput, self.cnicInput, self.SuggestedTime, self.Above60Box, self.SeatsBox, 
             self.Age2t18Box, self.BookDetails, self.dobInput, self.departureInput, self.destinationInput, self.DateInput, self.TypeInput, self.timeInput]
        self.ViewReservationButton.clicked.connect(lambda: self.SetDefault(L))
        
        self.UpdateBookingFrame.hide()
        self.NameInputUpdate.textChanged.connect(lambda: self.CorrectName(self.NameInputUpdate, self.UpdateSubmit))
        self.cnicInputUpdate.textChanged.connect(lambda: self.CorrectCNIC(self.cnicInputUpdate, self.UpdateSubmit))
        self.UpdateSubmit.clicked.connect(self.UpdateReservation)
        self.MenuButtonUpdateTab.clicked.connect(lambda: self.ReturnToMenu(self.UpdateBookingFrame, self.NameInputUpdate, self.cnicInputUpdate))
        self.departureInputUpdate.currentTextChanged.connect(lambda: self._updateDestination(self.departureInputUpdate, self.destinationInputUpdate))
        self.SeatsBoxUpdate.valueChanged.connect(lambda: self._update2to18(self.SeatsBoxUpdate.value(), self.Age2t18BoxUpdate, self.UpdateDetails))
        self.Age2t18BoxUpdate.valueChanged.connect(lambda: self._updateAbove60(self.Age2t18BoxUpdate.value(), self.Above60BoxUpdate))
        self.dobInputUpdate.hide()
        S = [self.FareFrameU, self.UpdateBookingFrame, self.AvailableComboUpdate, self.NameInputUpdate, self.cnicInputUpdate, self.SuggestedTime, self.Above60BoxUpdate, self.SeatsBoxUpdate, 
             self.Age2t18BoxUpdate, self.UpdateDetails, self.dobInputUpdate, self.departureInputUpdate, self.destinationInputUpdate, self.DateInputUpdate, self.TypeInputUpdate, self.timeInputUpdate]
        self.ViewReservationButtonUpdate.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.ViewReservationButtonUpdate.clicked.connect(lambda: self.ViewReservation(self.NameInputUpdate.text(), self.cnicInputUpdate.text(), out, self.ViewTicketFrame))
        self.ViewReservationButtonUpdate.clicked.connect(lambda: self.SetDefault(S))
        self.FareFrameU.hide()
        
        self.ViewTicketFrame.hide()
        self.NameInputBox.textChanged.connect(lambda: self.CorrectName(self.NameInputBox, self.ViewSubmit))
        self.cnicInputBox.textChanged.connect(lambda: self.CorrectCNIC(self.cnicInputBox, self.ViewSubmit))
        self.ViewSubmit.clicked.connect(lambda: self.ViewReservation(self.NameInputBox.text(), self.cnicInputBox.text(), out, self.ViewTicketFrame))
        self.MenuButtonViewTab.clicked.connect(lambda: self.ReturnToMenu(self.ViewTicketFrame, self.NameInputBox, self.cnicInputBox))
        
        self.CancelTicketFrame.hide()
        self.NameInputCancel.textChanged.connect(lambda: self.CorrectName(self.NameInputCancel, self.CancelSubmit))
        self.cnicInputCancel.textChanged.connect(lambda: self.CorrectCNIC(self.cnicInputCancel, self.CancelSubmit))
        self.CancelSubmit.clicked.connect(self.CancelBooking)
        self.MenuButtonCancelTab.clicked.connect(lambda: self.ReturnToMenu(self.CancelTicketFrame, self.NameInputCancel, self.cnicInputCancel))
                  
    def CorrectName(self, name, button):
        if not all(x.isalpha() or x.isspace() for x in name.text()) or (name.text() == ""):
            name.setStyleSheet("border: 1px solid red;")
            button.setEnabled(False)
        else:
            name.setStyleSheet("border: 1px solid black;")
            button.setEnabled(True)
            
    def CorrectCNIC(self, cnic, button):
        if not all(x.isdigit() for x in cnic.text()) or len(cnic.text()) < 13 or (cnic.text() == ""):
            cnic.setStyleSheet("border: 1px solid red;")
            button.setEnabled(False)
        else:
            cnic.setStyleSheet("border: 1px solid black;")
            button.setEnabled(True)
    
    def ReturnToMenu(self, frame, name, cnic):
        frame.hide()
        name.setText("")
        cnic.setText("")
        name.setStyleSheet("border: 1px solid black;")
        cnic.setStyleSheet("border: 1px solid black;")
        self.tabWidget.setCurrentIndex(0)
        self.message.setText("")
        
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
            with open("Trains.txt","r") as file:
                train100=file.readlines()
                for i in train100:
                    if '"Type": "'+t_type.lower()+'", "day": "'+day+'", "time": '+'"'+time+'", '+ '"'+dept.lower()+'": "'+dest.lower()+'"' in i:
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
        with open("schedule.txt") as op:
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
        
    def ViewReservation(self, name, cnic, outputs, frame):
        row = self.ReadFile(name, cnic)
        if row == []:
            return None
        else:
            frame.show()
            outputs[0].setText(row[0])
            outputs[1].setText(row[1])
            outputs[2].setText(row[3])
            outputs[3].setText(row[4])
            outputs[4].setText(row[5])
            outputs[5].setText(row[6])
            outputs[6].setText(row[7])
            outputs[7].setText(row[8])
            outputs[8].setText(row[14])
    
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
        name = self.NameInputCancel.text()
        cnic = self.cnicInputCancel.text()
        row = self.ReadFile(name, cnic)
        outCancel = [self.cnicOutputCancel, self.NameOutputCancel, self.FromOutputCancel, self.ToOutputCancel, 
                     self.DateOutputCancel, self.DayOutputCancel, self.TimeOutputCancel, 
                     self.TypeOutputCancel, self.SeatsOutputCancel]
        
        if row == []:
            pass
        else:
            self.ViewReservation(name, cnic, outCancel, self.CancelTicketFrame)
            self.message.setText("Your Booking has been successfully cancelled! A refund of 50% has been transferred to your account.")
            self.RemoveBooking(row)
        
schedule_maker()
trains_maker()
try:
    f = open("TrainReservation.txt", "x")
except:
    pass
else:
    customer_information()
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()