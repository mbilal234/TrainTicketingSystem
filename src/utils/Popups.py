from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Popup(QtWidgets.QWidget):
	def missing_popup(self, message):
		msg = QMessageBox()
		msg.setWindowTitle("Missing Information")
		msg.setText(message)
		msg.setIcon(QMessageBox.Warning)
		msg.setStandardButtons(QMessageBox.Ok)
		
		msg.exec_()

	def cancel_popup(self, app):
		msg = QMessageBox()
		msg.setWindowTitle("Cancel Booking")
		msg.setText("Do you want to cancel the booking?")
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		msg.setDefaultButton(QMessageBox.No)
		
		msg.exec_()
		button = msg.clickedButton()
		if button is not None:
			return button.text()

	def success_popup(self, message):
		msg = QMessageBox()
		msg.setWindowTitle("Success")
		msg.setText(message)
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Ok)
		
		msg.exec_()

	def error_popup(self, message):
		msg = QMessageBox()
		msg.setWindowTitle("Error")
		msg.setText(message)
		msg.setIcon(QMessageBox.Critical)
		msg.setStandardButtons(QMessageBox.Ok)
		
		msg.exec_()