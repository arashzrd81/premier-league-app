import random
import requests
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, QTimer, Qt
from Check import Check
from Error import Error
from Execution import Execution
from SendEmail import SendEmail
from ClickableLabels import ClickableLabels



# SignUp class
class SignUp():

    # constructor
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.label = [None]*14
        self.lineEdit = [None]*3
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the Create... text
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(35, 200, 500, 40))
        self.label[0].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:15pt; font-weight:600; color:#ffffff;\">Create your Premier League App account :</span></p></body></html>"))

        # set the pink rectangles for backgrounds of the requested items
        pinkRectangleUrl = "https://i.postimg.cc/fThpk9fB/pink-rectangle.png"
        pinkRectangleImg = QImage()
        pinkRectangleImg.loadFromData(requests.get(pinkRectangleUrl).content)
        for i in range(1, 4):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(30, 320 + 100*(i-1), 110, 30))
            self.label[i].setPixmap(QPixmap(pinkRectangleImg))

        # set the requested items and their text
        for i in range(4, 7):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(35, 320 + 100*(i-4), 100, 30))
            if i == 4:
                self.label[4].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Username :</span></p></body></html>"))
            elif i == 5:
                self.label[5].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Email :</span></p></body></html>"))
            else:
                self.label[6].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Password :</span></p></body></html>"))

        # set the @gmail.com text
        self.label[7] = QLabel(Form)
        self.label[7].setGeometry(QRect(310, 420, 100, 30))
        self.label[7].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; color:#ffffff;\">@gmail.com</span></p></body></html>"))

        # set the unhide icon and clickable it
        unhideIconUrl = "https://i.postimg.cc/FFJyJknk/unhide-icon.png"
        unhideIconImg = QImage()
        unhideIconImg.loadFromData(requests.get(unhideIconUrl).content)
        self.label[8] = ClickableLabels(Form)
        self.label[8].setGeometry(QRect(310, 520, 30, 30))
        self.label[8].setPixmap(QPixmap(unhideIconImg))
        self.label[8].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[8].clicked.connect(lambda: self.unhide())

        # set the empty labels for possible user error entering items and show ticks
        tickUrl = "https://i.postimg.cc/mhfWd1Qg/green-tick.png"
        tickImg = QImage()
        tickImg.loadFromData(requests.get(tickUrl).content)
        for i in range(9, 12):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(135, 350 + 100*(i-9), 445, 30))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[12] = ClickableLabels(Form)
        self.label[12].setGeometry(QRect(5, 5, 30, 30))
        self.label[12].setPixmap(QPixmap(backArrowImg))
        self.label[12].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[12].clicked.connect(lambda: self.back())

        # set the Done button
        doneButtonUrl = "https://i.postimg.cc/8c4Hpbn8/done-button.png"
        doneButtonImg = QImage()
        doneButtonImg.loadFromData(requests.get(doneButtonUrl).content)
        self.label[13] = ClickableLabels(Form)
        self.label[13].setGeometry(QRect(498, 630, 90, 30))
        self.label[13].setPixmap(QPixmap(doneButtonImg))
        self.label[13].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[13].clicked.connect(lambda: self.check(tickImg))

        # set the edit lines for requested items
        for i in range(3):
            self.lineEdit[i] = QLineEdit(Form)
            self.lineEdit[i].setGeometry(QRect(135, 320 + i*100, 170, 30))
            self.lineEdit[i].setFont(QFont("Times", 12))
            if i == 2:
                self.lineEdit[2].setEchoMode(QLineEdit.Password)

    # unhide method that is unhide characters of password when user want
    def unhide(self):
        try:
            self.lineEdit[2].setEchoMode(QLineEdit.Normal)
            hideIconUrl = "https://i.postimg.cc/1tVq6bM1/hide-icon.png"
            hideIconImg = QImage()
            hideIconImg.loadFromData(requests.get(hideIconUrl).content)
            self.label[8].setPixmap(QPixmap(hideIconImg))
            self.label[8].clicked.connect(lambda: self.hide())
        except:
            obj = Error()
            obj.showError()

    # hide method that is hide characters of password when user want
    def hide(self):
        try:
            self.lineEdit[2].setEchoMode(QLineEdit.Password)
            unhideIconUrl = "https://i.postimg.cc/FFJyJknk/unhide-icon.png"
            unhideIconImg = QImage()
            unhideIconImg.loadFromData(requests.get(unhideIconUrl).content)
            self.label[8].setPixmap(QPixmap(unhideIconImg))
            self.label[8].clicked.connect(lambda: self.unhide())
        except:
            obj = Error()
            obj.showError()

    # if the user clicks on Back button, StartMenu window runs
    def back(self):
        executor = Execution(self.mainWindow, "StartMenu")
        executor.execute()

    # if the user clicks on Done button, input data is checked
    def check(self, tickImg):
        try:
            obj = Check()
            quorum = obj.checkSignUp(
                         self.label,
                         self.getUsername(),
                         self.getEmail(),
                         self.getPassword()
                     )
        except:
            obj = Error()
            obj.showError()

        # if all required items are filled in correctly, should verify the user email address
        if quorum == 3:
            self.label[7].clear()
            self.label[8].clear()
            for i in range(9, 12):
                self.label[i].move(310, 320 + 100*(i-9))
                self.label[i].setPixmap(QPixmap(tickImg))
            QTimer.singleShot(1, lambda: self.verification())

    # verification method that sends a verify code (random) to email address of the user and execute Verification window
    def verification(self):
        verifyCode = self.getRandomNumber()
        userData = {
            "username": self.getUsername(),
            "email": self.getEmail(),
            "password": self.getPassword()
        }

        # execute Verification
        executor = Execution(self.mainWindow, "Verification")
        executor.execute(
            verifyCode=verifyCode,
            userData=userData
        )

        # create an object from SendEmail to send generated verify code
        obj = SendEmail()
        obj.sendEmail(
            username=self.getUsername(),
            email=self.getEmail() + "@gmail.com",
            subject="Verify Code",
            verifyCode=verifyCode
        )

    # getRandomNumber method that returns a 7-digit random number to send (vrify code)
    def getRandomNumber(self):
        return str(random.randint(10**6, 9999999))

    # getUsername method that returns the input username
    def getUsername(self):
        return self.lineEdit[0].text()

    # getEmail method that returns the input email (without @gmail.com)
    def getEmail(self):
        return self.lineEdit[1].text()

    # getPassword method that returns the input password
    def getPassword(self):
        return self.lineEdit[2].text()