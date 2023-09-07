import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QCoreApplication



# Error class
class Error():

    # showError method that shows error
    def showError(self):
        Form = QMessageBox()

        # perform graphic items related to the network connection error (icon, buttons, text, ...)
        Form.setWindowTitle("Unexpected Error")
        Form.setIcon(QMessageBox.Critical)
        translate = QCoreApplication.translate
        Form.setText(translate(
            "Form",
            """<html><head/><body>
            <p><span style=\" font-size:10pt; color:#000000;\">Sorry, an unknown and unexpected error occurred.</span></p>
            <p><span style=\" font-size:10pt; color:#000000;\">There may be a problem with your internet connection.</span></p>
            <p><span style=\" font-size:10pt; color:#000000;\">Please execute Premier League App from the beginning.</span></p>
            </body></html>"""
        ))

        clickedButton = Form.exec_()

        # if the user click on Ok button, the app ends
        if clickedButton == QMessageBox.Ok:
            sys.exit()