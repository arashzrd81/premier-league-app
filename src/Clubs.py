import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Database import Database
from Execution import Execution
from ClickableLabels import ClickableLabels



# Clubs class
class Clubs():

    # constructor
    def __init__(self, mainWindow, userData):
        self.mainWindow = mainWindow
        self.__userData = userData
        self.label = [None]*41
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the Choose... text
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(30, 150, 500, 30))
        self.label[0].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:15pt; font-weight:600; color:#ffffff;\">Choose your favorite club :</span></p></body></html>"))

        # get clubs name and clubs logo link (50*50)
        clubsName, clubsLogoLink = self.scrape()

        # set the clubs logo (50*50)
        for i in range(1, 21):
            self.label[i] = ClickableLabels(Form)
            clubLogoUrl = clubsLogoLink[i-1]
            img = QImage()
            img.loadFromData(requests.get(clubLogoUrl).content)
            self.label[i].setPixmap(QPixmap(img))
            self.label[i].setCursor(QCursor(Qt.PointingHandCursor))
            self.label[i].setStyleSheet("QLabel::hover {background-color: #ff2883;}")
            self.label[i].setToolTip(clubsName[i-1])
            if 1 <= i <= 5:
                self.label[i].setGeometry(QRect(30, 200 + 100*(i-1), 130, 60))
            elif 6 <= i <= 10:
                self.label[i].setGeometry(QRect(165, 200 + 100*(i-6), 130, 60))
            elif 11 <= i <= 15:
                self.label[i].setGeometry(QRect(310, 200 + 100*(i-11), 130, 60))
            else:
                self.label[i].setGeometry(QRect(445, 200 + 100*(i-16), 130, 60))

        # set the clubs name
        for i in range(21, 41):
            self.label[i] = QLabel(Form)
            self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:9pt; color:#ffffff;\">%s</span></p></body></html>" %clubsName[i-21]))
            if 21 <= i <= 25:
                self.label[i].setGeometry(QRect(85, 210 + 100*(i-21), 70, 40))
            elif 26 <= i <= 30:
                self.label[i].setGeometry(QRect(220, 210 + 100*(i-26), 80, 40))
            elif 31 <= i <= 35:
                self.label[i].setGeometry(QRect(365, 210 + 100*(i-31), 70, 40))
            else:
                self.label[i].setGeometry(QRect(495, 210 + 100*(i-36), 80, 40))

        # clickable the each related clubs section
        self.label[1].clicked.connect(lambda: self.saveData(clubsName, 1))
        self.label[2].clicked.connect(lambda: self.saveData(clubsName, 2))
        self.label[3].clicked.connect(lambda: self.saveData(clubsName, 3))
        self.label[4].clicked.connect(lambda: self.saveData(clubsName, 4))
        self.label[5].clicked.connect(lambda: self.saveData(clubsName, 5))
        self.label[6].clicked.connect(lambda: self.saveData(clubsName, 6))
        self.label[7].clicked.connect(lambda: self.saveData(clubsName, 7))
        self.label[8].clicked.connect(lambda: self.saveData(clubsName, 8))
        self.label[9].clicked.connect(lambda: self.saveData(clubsName, 9))
        self.label[10].clicked.connect(lambda: self.saveData(clubsName, 10))
        self.label[11].clicked.connect(lambda: self.saveData(clubsName, 11))
        self.label[12].clicked.connect(lambda: self.saveData(clubsName, 12))
        self.label[13].clicked.connect(lambda: self.saveData(clubsName, 13))
        self.label[14].clicked.connect(lambda: self.saveData(clubsName, 14))
        self.label[15].clicked.connect(lambda: self.saveData(clubsName, 15))
        self.label[16].clicked.connect(lambda: self.saveData(clubsName, 16))
        self.label[17].clicked.connect(lambda: self.saveData(clubsName, 17))
        self.label[18].clicked.connect(lambda: self.saveData(clubsName, 18))
        self.label[19].clicked.connect(lambda: self.saveData(clubsName, 19))
        self.label[20].clicked.connect(lambda: self.saveData(clubsName, 20))

    # scrape method that does scrape operation and returns clubs name and clubs logo link (50*50)
    def scrape(self):

        # connect to page of Premier League for get the data and see it as html form
        page = requests.get("https://www.premierleague.com/matchweek/6662/table")
        soup = BeautifulSoup(page.content, "html.parser")

        # get the clubs data
        dataList = [None]*100
        dataList = soup.select("td")

        # get the clubs name
        clubsName = [dataList[i].getText().strip() for i in range(100) if i%5 == 1]

        # get the clubs logo link (50*50)
        clubsLogoLink = soup.findAll("img", {"class": "badge-image badge-image--20 js-badge-image"})
        clubsLogoLink = [clubsLogoLink[i].get("src").replace("/20", "/50") for i in range(20)]

        return clubsName, clubsLogoLink

    # saveData method that connect to database and save the data of the user
    def saveData(self, clubsName, count):

        # get the favorite club of the user
        self.__userData["favoriteClub"] = clubsName[count-1]

        # create an object from Database to save data
        database = Database()
        database.connectToDatabase()
        database.insert(
            self.__userData["username"],
            self.__userData["email"] + "@gmail.com",
            self.__userData["password"],
            self.__userData["favoriteClub"]
        )

        self.account()

    # account method that execute Account window
    def account(self):
        executor = Execution(self.mainWindow, "Account")
        executor.execute(userData=self.__userData)