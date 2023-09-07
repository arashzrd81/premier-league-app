import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Execution import Execution
from ClickableLabels import ClickableLabels



# Fixture class
class Fixture():

    # constructor
    def __init__(self, mainWindow, userData):
        self.mainWindow = mainWindow
        self.__userData = userData
        self.label = [None]*83
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # get matchweek count and clubs name and clubs logo link (25*25)
        matchweek, clubsName, clubsLogoLink = self.scrape()

        # set the light green rectangle for background of matchweek
        greenRectangleUrl = "https://i.postimg.cc/Sx3Q81m4/green-rectangle.png"
        greenRectangleImg = QImage()
        greenRectangleImg.loadFromData(requests.get(greenRectangleUrl).content)
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(220, 165, 160, 35))
        self.label[0].setPixmap(QPixmap(greenRectangleImg))

        # set the Matchweek <count> (in light green rectangle)
        self.label[1] = QLabel(Form)
        self.label[1].setGeometry(QRect(240, 172, 130, 20))
        self.label[1].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:13pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %matchweek))

        # set the white squars for background of clubs logo
        whitePageUrl = "https://i.postimg.cc/vBJQH96K/white-page.png"
        whitePageImg = QImage()
        whitePageImg.loadFromData(requests.get(whitePageUrl).content)
        for i in range(2, 22):
            self.label[i] = QLabel(Form)
            self.label[i].setPixmap(QPixmap(whitePageImg))
            if 2 <= i <= 11:
                self.label[i].setGeometry(QRect(40, 220 + 44*(i-2), 35, 35))
            else:
                self.label[i].setGeometry(QRect(525, 220 + 44*(i-12), 35, 35))

        # set the pink rectangles for background of clubs name
        pinkRectangleUrl = "https://i.postimg.cc/fThpk9fB/pink-rectangle.png"
        pinkRectangleImg = QImage()
        pinkRectangleImg.loadFromData(requests.get(pinkRectangleUrl).content)
        for i in range(22, 42):
            self.label[i] = QLabel(Form)
            self.label[i].setPixmap(QPixmap(pinkRectangleImg))
            if 22 <= i <= 31:
                self.label[i].setGeometry(QRect(75, 220 + 44*(i-22), 220, 35))
            else:
                self.label[i].setGeometry(QRect(305, 220 + 44*(i-32), 220, 35))

        # set the clubs logo (25*25)
        for i in range(42, 62):
            self.label[i] = QLabel(Form)
            clubLogoUrl = clubsLogoLink[i-42]
            img = QImage()
            img.loadFromData(requests.get(clubLogoUrl).content)
            self.label[i].setPixmap(QPixmap(img))
            if 42 <= i <= 51:
                self.label[i].setGeometry(QRect(45, 225 + 44*(i-42), 25, 25))
            else:
                self.label[i].setGeometry(QRect(530, 225 + 44*(i-52), 25, 25))

        # set the clubs name
        for i in range(62, 82):
            self.label[i] = QLabel(Form)
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %clubsName[i-62]))
            if 62 <= i <= 71:
                self.label[i].setGeometry(QRect(80, 227 + 44*(i-62), 205, 25))
            else:
                self.label[i].setGeometry(QRect(310, 227 + 44*(i-72), 205, 25))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[82] = ClickableLabels(Form)
        self.label[82].setGeometry(QRect(5, 5, 30, 30))
        self.label[82].setPixmap(QPixmap(backArrowImg))
        self.label[82].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[82].clicked.connect(lambda: self.back())

    # scrape method that does scrape operation and returns matchweek count clubs name and clubs logo link (25*25)
    def scrape(self):

        # connect to page of Premier League for get the data and see it as html form
        page = requests.get("https://www.premierleague.com/")
        soup = BeautifulSoup(page.content, "html.parser")

        # get the matchweek count
        matchweek = soup.find("div", {"class": "week"}).getText()

        # get the clubs name
        data = soup.select("abbr")
        clubsName = [data[i].get("title").strip() for i in range(20) if i%2 == 0]
        temp = [data[i].get("title").strip() for i in range(20) if i%2 == 1]
        clubsName.extend(temp)

        # get the clubs logo
        data = soup.findAll("span", {
                        "class": "badge badge-image-container",
                        "data-widget": "club-badge-image",
                        "data-size": "25"
                        })
        del data[20:]
        irregular = [imgTag.get("src") for spanTag in data for imgTag in spanTag.findAll("img")]
        clubsLogoLink = [irregular[i] for i in range(20) if i%2 == 0 ]
        temp = [irregular[i] for i in range(20) if i%2 == 1]
        clubsLogoLink.extend(temp)

        return matchweek, clubsName, clubsLogoLink

    # if the user clicks on Back button, Account window runs
    def back(self):
        executor = Execution(self.mainWindow, "Account")
        executor.execute(userData=self.__userData)