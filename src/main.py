from peripheries import CustomerInformation, GUI, ScheduleMaker, Train, TrainsMaker
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import *
import sys

def main():    
    schedule_maker = ScheduleMaker.ScheduleMaker()
    schedule_maker.generate_schedule()
    schedule_maker.read_schedule()
    # Modify the schedule list if needed
    schedule_maker.save_schedule()
    trains_maker = TrainsMaker.TrainsMaker()
    trains = trains_maker.generate_train_objects()
    trains_maker.save_trains_to_file(trains)
    try:
        f = open("TrainReservation.txt", "x")
    except:
        pass
    else:
        CustomerInformation.CustomerInformation()
    app = QtWidgets.QApplication(sys.argv)
    window = GUI.MainWindow()
    window.show()
    app.exec_()

main()