import requests
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget
from PyQt5.QtGui import QCursor, QFont, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, QTimer, Qt
from Check import Check
from Error import Error
from Database import Database
from Execution import Execution
from SendEmail import SendEmail
from DeleteAccount import DeleteAccount
from ClickableLabels import ClickableLabels



# AccountSettings class
class AccountSettings():

    # constructor
    def __init__(self, mainWindow, userData):
        self.mainWindow = mainWindow
        self.__userData = userData
        self.__username = self.__userData["username"]
        self.__email = self.__userData["email"]
        self.label = [None]*17
        self.lineEdit = [None]*3
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the Change Password text
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(35, 200, 500, 40))
        self.label[0].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:15pt; font-weight:600; color:#ffffff;\">Change Password :</span></p></body></html>"))

        # set the pink rectangles for backgrounds of the requested items
        pinkRectangleUrl = "https://i.postimg.cc/fThpk9fB/pink-rectangle.png"
        pinkRectangleImg = QImage()
        pinkRectangleImg.loadFromData(requests.get(pinkRectangleUrl).content)
        for i in range(1, 4):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(30, 270 + 80*(i-1), 200, 30))
            self.label[i].setPixmap(QPixmap(pinkRectangleImg))

        # set the requested items and their text
        for i in range(4, 7):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(35, 270 + 80*(i-4) , 200, 30))
            if i == 4:
                self.label[4].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Current Password :</span></p></body></html>"))
            elif i == 5:
                self.label[5].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">New Password :</span></p></body></html>"))
            else:
                self.label[6].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">New Password, again :</span></p></body></html>"))

        # set the unhide icons and clickable them
        unhideIconUrl = "https://i.postimg.cc/FFJyJknk/unhide-icon.png"
        unhideIconImg = QImage()
        unhideIconImg.loadFromData(requests.get(unhideIconUrl).content)
        for i in range(7, 10):
            self.label[i] = ClickableLabels(Form)
            self.label[i].setGeometry(QRect(405, 270 + 80*(i-7), 30, 30))
            self.label[i].setPixmap(QPixmap(unhideIconImg))
            self.label[i].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[7].clicked.connect(lambda: self.unhide(7))
        self.label[8].clicked.connect(lambda: self.unhide(8))
        self.label[9].clicked.connect(lambda: self.unhide(9))

        # set the empty labels for possible user error entering items
        for i in range(10, 13):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(230, 300 + 80*(i-10), 350, 30))

        # set the Password Changed Successfully message text
        passwordChangedMessageUrl = "https://i.postimg.cc/bNCQJrLt/password-changed-message.png"
        passwordChangedMessageImg = QImage()
        passwordChangedMessageImg.loadFromData(requests.get(passwordChangedMessageUrl).content)
        self.label[13] = QLabel(Form)
        self.label[13].setGeometry(QRect(35, 500, 240, 40))

        # set the Delete My Account button
        deleteAccountButtonUrl = "https://i.postimg.cc/LsXfMpjV/delete-account-button.png"
        deleteAccountButtonImg = QImage()
        deleteAccountButtonImg.loadFromData(requests.get(deleteAccountButtonUrl).content)
        self.label[14] = ClickableLabels(Form)
        self.label[14].setGeometry(QRect(35, 560, 240, 40))
        self.label[14].setPixmap(QPixmap(deleteAccountButtonImg))
        self.label[14].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[14].clicked.connect(lambda: self.deleteAccount(Form))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[15] = ClickableLabels(Form)
        self.label[15].setGeometry(QRect(5, 5, 30, 30))
        self.label[15].setPixmap(QPixmap(backArrowImg))
        self.label[15].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[15].clicked.connect(lambda: self.back())

        # set the Done button
        doneButtonUrl = "https://i.postimg.cc/8c4Hpbn8/done-button.png"
        doneButtonImg = QImage()
        doneButtonImg.loadFromData(requests.get(doneButtonUrl).content)
        self.label[16] = ClickableLabels(Form)
        self.label[16].setGeometry(QRect(498, 630, 90, 30))
        self.label[16].setPixmap(QPixmap(doneButtonImg))
        self.label[16].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[16].clicked.connect(lambda: self.check(passwordChangedMessageImg))

        # set the edit lines for requested items
        for i in range(3):
            self.lineEdit[i] = QLineEdit(Form)
            self.lineEdit[i].setGeometry(QRect(230, 270 + i*80, 170, 30))
            self.lineEdit[i].setFont(QFont("Times", 12))
            self.lineEdit[i].setEchoMode(QLineEdit.Password)

    # unhide method that is unhide characters of password when user want
    def unhide(self, num):
        try:
            self.lineEdit[num-7].setEchoMode(QLineEdit.Normal)
            hideIconUrl = "https://i.postimg.cc/1tVq6bM1/hide-icon.png"
            hideIconImg = QImage()
            hideIconImg.loadFromData(requests.get(hideIconUrl).content)
            self.label[num].setPixmap(QPixmap(hideIconImg))
            self.label[num].clicked.connect(lambda: self.hide())
        except:
            obj = Error()
            obj.showError()

    # hide method that is hide characters of password when user want
    def hide(self, num):
        try:
            self.lineEdit[num-7].setEchoMode(QLineEdit.Password)
            unhideIconUrl = "https://i.postimg.cc/FFJyJknk/unhide-icon.png"
            unhideIconImg = QImage()
            unhideIconImg.loadFromData(requests.get(unhideIconUrl).content)
            self.label[num].setPixmap(QPixmap(unhideIconImg))
            self.label[num].clicked.connect(lambda: self.unhide())
        except:
            obj = Error()
            obj.showError()

    # deleteAccount method that display a message to see if the user is sure of deleting his/her account
    def deleteAccount(self, Form):
        try:
            deleteAccountWindow = QWidget()
            obj = DeleteAccount(self.mainWindow, Form, self.__username, self.__email)
            obj.setupUi(deleteAccountWindow)
            deleteAccountWindow.show()
        except:
            obj = Error()
            obj.showError()

    # if the user clicks on back arrow sign, Account window runs
    def back(self):
        executor = Execution(self.mainWindow, "Account")
        executor.execute(userData=self.__userData)

    # if the user clicks on Done button, input passwords are checked
    def check(self, PasswordChangedMessageImg):
        try:
            obj = Check()
            quorum = obj.checkChangePassword(
                         self.__username,
                         self.label,
                         self.lineEdit[0].text(),
                         self.lineEdit[1].text(),
                         self.lineEdit[2].text()
                     )
        except:
            obj = Error()
            obj.showError()

        # if all required items are filled in correctly, should does change password operation
        if quorum == 3:
            self.label[13].setPixmap(QPixmap(PasswordChangedMessageImg))
            QTimer.singleShot(1500, lambda: self.updatePassword())

    # updatePassword method that update the password of the user
    def updatePassword(self):
        self.label[13].clear()

        # create an object from Database to save data
        database = Database()
        database.connectToDatabase()
        database.updatePassword(self.__username, self.lineEdit[1].text())

        # create an object from SendEmail to send change password message
        obj = SendEmail()
        obj.sendEmail(
            username=self.__username,
            email=self.__email,
            subject="Change Password"
        )