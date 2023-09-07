import requests
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from PyQt5.QtGui import QCursor, QIcon, QImage, QPixmap
from Database import Database
from Execution import Execution
from SendEmail import SendEmail
from ClickableLabels import ClickableLabels



# DeleteAccount class
class DeleteAccount():

    # constructor
    def __init__(self, mainWindow, accountSettingsWindow, username, email):
        self.mainWindow = mainWindow
        self.accountSettingsWindow = accountSettingsWindow
        self.__username = username
        self.__email = email
        self.label = [None]*4
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the size and name and icon of the window bar
        Form.resize(470, 120)
        Form.setWindowTitle(self.translate("Form", "Delete Account"))
        url = "https://i.postimg.cc/C1XY0nG0/lion.png"
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(url).content)
        icon = QIcon(pixmap)
        Form.setWindowIcon(icon)

        # set the purple theme
        url = "https://i.postimg.cc/mkVxmdbm/purple-theme.png"
        img = QImage()
        img.loadFromData(requests.get(url).content)
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(0, 0, 470, 120))
        self.label[0].setPixmap(QPixmap(img))

        # set the Are... text
        self.label[1] = QLabel(Form)
        self.label[1].setGeometry(QRect(20, 15, 440, 30))
        self.label[1].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; color:#ffffff;\">Are you sure you want to delete your account ?</span></p></body></html>"))

        # set the Delete button
        deleteUrl = "https://i.postimg.cc/fLnPrB9D/delete-button.png"
        deleteImg = QImage()
        deleteImg.loadFromData(requests.get(deleteUrl).content)
        self.label[2] = ClickableLabels(Form)
        self.label[2].setGeometry(QRect(295, 85, 75, 23))
        self.label[2].setPixmap(QPixmap(deleteImg))
        self.label[2].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[2].clicked.connect(lambda: self.deleteAccount(Form))

        # set the No button
        noUrl = "https://i.postimg.cc/gjK1R8rd/no-button.png"
        noImg = QImage()
        noImg.loadFromData(requests.get(noUrl).content)
        self.label[3] = ClickableLabels(Form)
        self.label[3].setGeometry(QRect(380, 85, 75, 23))
        self.label[3].setPixmap(QPixmap(noImg))
        self.label[3].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[3].clicked.connect(lambda: self.back(Form))

    # deleteAccount method that connect to the database and remove the user account
    def deleteAccount(self, Form):

        # create an object from Database to save data
        database = Database()
        database.connectToDatabase()
        database.deleteAccount(self.__username)

        # close DeleteAccount and AccountSettings windows
        Form.close()
        self.accountSettingsWindow.close()

        # create an object from SendEmail to send delete account message
        obj = SendEmail()
        obj.sendEmail(
            username=self.__username,
            email=self.__email,
            subject="Delete Account"
        )

        # after delete account of the user, StartMenu window runs
        executor = Execution(self.mainWindow, "StartMenu")
        executor.execute()

    # if the user clicks on No button, Delete Account window will close
    def back(self, Form):
        Form.close()