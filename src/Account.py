import requests
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Database import Database
from Execution import Execution
from ClickableLabels import ClickableLabels



# Account class
class Account():

    # constructor
    def __init__(self, mainWindow, userData):
        self.mainWindow = mainWindow
        self.__username = userData["username"]
        self.label = [None]*7
        self.line = [None]*3
        self.translate = QCoreApplication.translate

        # get the user data
        database = Database()
        database.connectToDatabase()
        self.__data = database.specialSelect(self.__username)
        self.__userData = {
            "username": self.__data[0][0],
            "email": self.__data[0][1],
            "password": self.__data[0][2],
            "favoriteClub": self.__data[0][3]
        }

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the user icon (account settings)
        userIconUrl = "https://i.postimg.cc/BZx80TVp/user-icon.png"
        userIconImg = QImage()
        userIconImg.loadFromData(requests.get(userIconUrl).content)
        self.label[0] = ClickableLabels(Form)
        self.label[0].setGeometry(QRect(567, 7, 25, 25))
        self.label[0].setPixmap(QPixmap(userIconImg))
        self.label[0].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[0].setToolTip("Account Settings")
        self.label[0].clicked.connect(lambda: self.accountSettings())

        # set the club logo (200*200) that the user is in favor of
        clubLogoUrl = self.searchLogo()
        clubLogoImg = QImage()
        clubLogoImg.loadFromData(requests.get(clubLogoUrl).content)
        self.label[1] = QLabel(Form)
        self.label[1].setGeometry(QRect(30, 150, 210, 210))
        self.label[1].setPixmap(QPixmap(clubLogoImg))
        self.label[1].setToolTip(self.__userData["favoriteClub"])

        # set the Hi... text
        self.label[2] = QLabel(Form)
        self.label[2].setGeometry(QRect(250, 170, 320, 171))
        self.label[2].setText(self.translate(
            "Form",
            """<html><head/><body><p><span style=\" font-size:14pt; color:#ffffff;\">Hi %s!</span></p>
            <p><span style=\" font-size:14pt; color:#ffffff;\">Welcome to %s fan club.</span></p>
            <p><span style=\" font-size:14pt; color:#ffffff;\">Here you can see the status of </span></p>
            <p><span style=\" font-size:14pt; color:#ffffff;\">%s in Premier League.</span></p>
            <p><span style=\" font-size:14pt; color:#ffffff;\">So, start now!</span></p>
            </body></html>""" %(self.__userData["username"], self.__userData["favoriteClub"] , self.__userData["favoriteClub"])
        ))

        # set the items related to the club
        for i in range(3, 7):
            self.label[i] = ClickableLabels(Form)
            self.label[i].setGeometry(QRect(205, 390 + 70*(i-3), 190, 45))
            self.label[i].setCursor(QCursor(Qt.PointingHandCursor))
            self.label[i].setStyleSheet("QLabel::hover {background-color: #ff2883;}")
            if i == 3:
                self.label[3].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Standings</span></p></body></html>"))
                self.label[3].clicked.connect(lambda: self.standings())
            elif i == 4:
                self.label[4].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Players</span></p></body></html>"))
                self.label[4].clicked.connect(lambda: self.players())
            elif i == 5:
                self.label[5].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Fixture</span></p></body></html>"))
                self.label[5].clicked.connect(lambda: self.fixture())
            else:
                self.label[6].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Stats</span></p></body></html>"))
                self.label[6].clicked.connect(lambda: self.stats())

        # set the horizontal lines
        for i in range(3):
            self.line[i] = QFrame(Form)
            self.line[i].setGeometry(QRect(185, 435 + i*70, 230, 20))
            self.line[i].setFrameShape(QFrame.HLine)
            self.line[i].setFrameShadow(QFrame.Sunken)

    # searchLogo method that search favorite club logo (200*200) of the user and returns that
    def searchLogo(self):

        # set the clubs logo link (200*200)
        clubsLogoLink = [
            "https://i.postimg.cc/CKTT0Mjx/Arsenal.png",
            "https://i.postimg.cc/Wp9B3wMK/Aston-Villa.png",
            "https://i.postimg.cc/cJdYDkWQ/Bournemouth.png",
            "https://i.postimg.cc/bNWHgRBW/Brentford.png",
            "https://i.postimg.cc/pdt77GH9/Brighton.png",
            "https://i.postimg.cc/QtfyFjW5/Burnley.png",
            "https://i.postimg.cc/pV1DVZRr/Chelsea.png",
            "https://i.postimg.cc/GmvgkFyb/Crystal-Palace.png",
            "https://i.postimg.cc/9fpxkcbS/Everton.png",
            "https://i.postimg.cc/nh2Ytf0d/Fulham.png",
            "https://i.postimg.cc/VkwpZZ1J/Leeds.png",
            "https://i.postimg.cc/nhTRRH0W/Leicester.png",
            "https://i.postimg.cc/N054dRyy/Liverpool.png",
            "https://i.postimg.cc/tgZ33yfW/Man-City.png",
            "https://i.postimg.cc/Y0kQBFSz/Man-Utd.png",
            "https://i.postimg.cc/qMPyyvtd/Newcastle.png",
            "https://i.postimg.cc/MZ4QJpmj/Norwich.png",
            "https://i.postimg.cc/Yqw1GCPn/Nott-m-Forest.png",
            "https://i.postimg.cc/FKLSfpdx/Southampton.png",
            "https://i.postimg.cc/vBwV5n5w/Spurs.png",
            "https://i.postimg.cc/5txHSYbD/Watford.png",
            "https://i.postimg.cc/c4L870tC/West-Ham.png",
            "https://i.postimg.cc/8zFJ34HV/Wolves.png"
        ]

        # search
        favoriteClubLogo = ''.join([clubsLogoLink[i] for i in range(len(clubsLogoLink)) if self.__userData["favoriteClub"].replace(' ', '-').replace("'", '-') in clubsLogoLink[i]])

        return favoriteClubLogo

    # if the user clicks on user icon, AccountSettings window runs
    def accountSettings(self):
        executor = Execution(self.mainWindow, "AccountSettings")
        executor.execute(userData=self.__userData)

    # if the user clicks on Standings, Standings window runs
    def standings(self):
        executor = Execution(self.mainWindow, "Standings")
        executor.execute(userData=self.__userData)

    # if the user clicks on Players, Players window runs
    def players(self):
        executor = Execution(self.mainWindow, "Players")
        executor.execute(userData=self.__userData)

    # if the user clicks on Fixture, Fixture window runs
    def fixture(self):
        executor = Execution(self.mainWindow, "Fixture")
        executor.execute(userData=self.__userData)

    # if the user clicks on Stats, Stats window runs
    def stats(self):
        executor = Execution(self.mainWindow, "Stats")
        executor.execute(userData=self.__userData)