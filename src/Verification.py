import random
import requests
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, QTimer, Qt
from Execution import Execution
from SendEmail import SendEmail
from ClickableLabels import ClickableLabels



# Verification class
class Verification():

    # constructor
    def __init__(self, mainWindow, verifyCode, userData):
        self.mainWindow = mainWindow
        self.__verifyCode = verifyCode
        self.__userData = userData
        self.label = [None]*6
        self.lineEdit = None
        self.translate = QCoreApplication.translate

        # for added security, not all email address characters are displayed
        self.__email = self.__userData["email"] + "@gmail.com"
        self.__email = list(self.__email)
        for i in range(len(self.__email) - 10):
            if (i != 0)  and (i != len(self.__email)-11):
                self.__email[i] = '*'
        self.__email = ''.join(self.__email)

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the We... text
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(50, 200, 500, 150))
        self.label[0].setText(self.translate(
            "Form",
            """<html><head/><body>
            <p><span style=\" font-size:13pt; font-weight:600; color:#ffffff;\">We have sent you a 7-digit verification code to your</span></p>
            <p><span style=\" font-size:13pt; font-weight:600; color:#ffffff;\">email at %s . To create</span></p>
            <p><span style=\" font-size:13pt; font-weight:600; color:#ffffff;\">your account and verify your email address, you need to</span></p>
            <p><span style=\" font-size:13pt; font-weight:600; color:#ffffff;\">enter the verification code in the box.</span></p>
            </body></html>""" %self.__email
        ))

        # set the Resend text and clickable it
        self.label[1] = ClickableLabels(Form)
        self.label[1].setGeometry(QRect(380, 310, 80, 30))
        self.label[1].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[1].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:13pt; font-weight:600; color:#ff2883;\">(Resend)</span></p></body></html>"))
        self.label[1].clicked.connect(lambda: self.resend())

        # set the Sent text
        self.label[2] = QLabel(Form)

        # set the empty label for possible user error entering verify code and show tick
        tickUrl = "https://i.postimg.cc/mhfWd1Qg/green-tick.png"
        tickImg = QImage()
        tickImg.loadFromData(requests.get(tickUrl).content)
        self.label[3] = QLabel(Form)
        self.label[3].setGeometry(QRect(270, 475, 100, 35))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[4] = ClickableLabels(Form)
        self.label[4].setGeometry(QRect(5, 5, 30, 30))
        self.label[4].setPixmap(QPixmap(backArrowImg))
        self.label[4].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[4].clicked.connect(lambda: self.back())

        # set the Done button
        doneButtonUrl = "https://i.postimg.cc/8c4Hpbn8/done-button.png"
        doneButtonImg = QImage()
        doneButtonImg.loadFromData(requests.get(doneButtonUrl).content)
        self.label[5] = ClickableLabels(Form)
        self.label[5].setGeometry(QRect(498, 630, 90, 30))
        self.label[5].setPixmap(QPixmap(doneButtonImg))
        self.label[5].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[5].clicked.connect(lambda: self.check(tickImg))

        # set the edit line
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setGeometry(QRect(255, 420, 90, 40))
        self.lineEdit.setFont(QFont("Times", 14, QFont.Bold))

    # if the user clicks on Resend, an distinc verify code is sent to email of the user
    def resend(self):

        # get new random number for resend
        self.__verifyCode = self.getRandomNumber()

        # create an object from SendEmail to send generated verify code
        obj = SendEmail()
        obj.sendEmail(
            username=self.__userData["username"],
            email=self.__userData["email"] + "@gmail.com",
            subject="Verify Code",
            verifyCode=self.__verifyCode
        )

        # remove Resend text and set the Sent text
        self.label[1].clear()
        self.label[2].setGeometry(QRect(380, 310, 80, 30))
        self.label[2].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:13pt; font-weight:600; color:#cccccc;\">(Sent)</span></p></body></html>"))

    # if the user clicks on Back button, SignUp window runs
    def back(self):
        executor = Execution(self.mainWindow, "SignUp")
        executor.execute()

    # if the user clicks on Done button, input code is checked
    def check(self, tickImg):
        if self.lineEdit.text() == self.__verifyCode:
            self.label[3].clear()
            self.label[3].move(355, 420)
            self.label[3].setPixmap(QPixmap(tickImg))
            QTimer.singleShot(1, lambda: self.clubs())
        else:
            self.label[3].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Incorrect</span></p></body></html>"))

    # clubs method that execute Clubs window
    def clubs(self):
        executor = Execution(self.mainWindow, "Clubs")
        executor.execute(userData=self.__userData)

    # getRandomNumber method that returns a 7-digit random number to send (vrify code)
    def getRandomNumber(self):
        return str(random.randint(10**6, 9999999))