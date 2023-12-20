def CorrectName(name, button):
    if not all(x.isalpha() or x.isspace() for x in name.text()) or (name.text() == ""):
        name.setStyleSheet(
            "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
        button.setEnabled(False)
    else:
        name.setStyleSheet(
            "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
        button.setEnabled(True)

def CorrectBooking(booking, button):
        if not all(x.isdigit() for x in booking.text()) or len(booking.text()) not in [4, 5] or (booking.text() == ""):
            booking.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
            button.setEnabled(False)
        else:
            booking.setStyleSheet(
                "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
            button.setEnabled(True)

def CorrectCNIC(cnic, button):
    if not all(x.isdigit() for x in cnic.text()) or len(cnic.text()) < 13 or (cnic.text() == ""):
        cnic.setStyleSheet(
            "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid red;")
        button.setEnabled(False)
    else:
        cnic.setStyleSheet(
            "color: rgb(13, 49, 58);background-color: rgb(232, 246, 239);border-radius: 10px;border: 1px solid black;")
        button.setEnabled(True)