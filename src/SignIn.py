import requests
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, QTimer, Qt
from Check import Check
from Error import Error
from Execution import Execution
from ClickableLabels import ClickableLabels



# SignIn class
class SignIn():

    # constructor
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.label = [None]*10
        self.lineEdit = [None]*2
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the Please... text
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(35, 200, 500, 100))
        self.label[0].setText(self.translate(
            "Form",
            """<html><head/><body><p><span style=\" font-size:15pt; font-weight:600; color:#ffffff;\">Please fill in the items:</span></p>
            </body></html>"""
        ))

        # set the pink rectangles for backgrounds of the requested items
        pinkRectangleUrl = "https://i.postimg.cc/fThpk9fB/pink-rectangle.png"
        pinkRectangleImg = QImage()
        pinkRectangleImg.loadFromData(requests.get(pinkRectangleUrl).content)
        for i in range(1, 3):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(30, 350 + 100*(i-1), 110, 30))
            self.label[i].setPixmap(QPixmap(pinkRectangleImg))

        # set the requested items and their text
        for i in range(3, 5):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(35, 350 + 100*(i-3), 100, 30))
            if i == 3:
                self.label[3].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Username :</span></p></body></html>"))
            else:
                self.label[4].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Password :</span></p></body></html>"))

        # set the unhide icon and clickable it
        unhideIconUrl = "https://i.postimg.cc/FFJyJknk/unhide-icon.png"
        unhideIconImg = QImage()
        unhideIconImg.loadFromData(requests.get(unhideIconUrl).content)
        self.label[5] = ClickableLabels(Form)
        self.label[5].setGeometry(QRect(310, 450, 30, 30))
        self.label[5].setPixmap(QPixmap(unhideIconImg))
        self.label[5].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[5].clicked.connect(lambda: self.unhide())

        # set the empty labels for possible user error entering items and show ticks
        tickUrl = "https://i.postimg.cc/mhfWd1Qg/green-tick.png"
        tickImg = QImage()
        tickImg.loadFromData(requests.get(tickUrl).content)
        for i in range(6, 8):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(135, 380 + 100*(i-6), 445, 30))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[8] = ClickableLabels(Form)
        self.label[8].setGeometry(QRect(5, 5, 30, 30))
        self.label[8].setPixmap(QPixmap(backArrowImg))
        self.label[8].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[8].clicked.connect(lambda: self.back())

        # set the Done button
        doneButtonUrl = "https://i.postimg.cc/8c4Hpbn8/done-button.png"
        doneButtonImg = QImage()
        doneButtonImg.loadFromData(requests.get(doneButtonUrl).content)
        self.label[9] = ClickableLabels(Form)
        self.label[9].setGeometry(QRect(498, 630, 90, 30))
        self.label[9].setPixmap(QPixmap(doneButtonImg))
        self.label[9].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[9].clicked.connect(lambda: self.check(tickImg))

        # set the edit lines for requested items
        for i in range(2):
            self.lineEdit[i] = QLineEdit(Form)
            self.lineEdit[i].setGeometry(QRect(135, 350 + i*100, 170, 30))
            self.lineEdit[i].setFont(QFont("Times", 12))
            if i == 1:
                self.lineEdit[1].setEchoMode(QLineEdit.Password)

    # unhide method that is unhide characters of password when user want
    def unhide(self):
        try:
            self.lineEdit[1].setEchoMode(QLineEdit.Normal)
            hideIconUrl = "https://i.postimg.cc/1tVq6bM1/hide-icon.png"
            hideIconImg = QImage()
            hideIconImg.loadFromData(requests.get(hideIconUrl).content)
            self.label[5].setPixmap(QPixmap(hideIconImg))
            self.label[5].clicked.connect(lambda: self.hide())
        except:
            obj = Error()
            obj.showError()

    # hide method that is hide characters of password when user want
    def hide(self):
        try:
            self.lineEdit[1].setEchoMode(QLineEdit.Password)
            unhideIconUrl = "https://i.postimg.cc/FFJyJknk/unhide-icon.png"
            unhideIconImg = QImage()
            unhideIconImg.loadFromData(requests.get(unhideIconUrl).content)
            self.label[5].setPixmap(QPixmap(unhideIconImg))
            self.label[5].clicked.connect(lambda: self.unhide())
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
            quorum = obj.checkSignIn(
                         self.label,
                         self.getUsername(),
                         self.getPassword()
                     )
        except:
            obj = Error()
            obj.showError()

        # if all required items are filled in correctly, the user signed in
        if quorum == 2:
            self.label[5].clear()
            for i in range(6, 8):
                self.label[i].move(310, 350 + 100*(i-6))
                self.label[i].setPixmap(QPixmap(tickImg))
            QTimer.singleShot(100, lambda: self.account())

    # account method that execute Account window
    def account(self):
        executor = Execution(self.mainWindow, "Account")
        executor.execute(userData={"username": self.getUsername()})

    # getUsername method that returns the input username
    def getUsername(self):
        return self.lineEdit[0].text()

    # getPassword method that returns the input password
    def getPassword(self):
        return self.lineEdit[1].text()