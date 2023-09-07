import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Execution import Execution
from ClickableLabels import ClickableLabels



# Standings class
class Standings():

    # constructor
    def __init__(self, mainWindow, userData):
        self.mainWindow = mainWindow
        self.__userData = userData
        self.favoriteClub = self.__userData["favoriteClub"]
        self.label = [None]*127
        self.line = None
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # get the necessary data for standings about clubs
        scrapedData = self.scrape()
        clubsLogoLink = scrapedData["clubsLogoLink"]
        clubsName = scrapedData["clubsName"]
        clubsMatchesCount = scrapedData["clubsMatchesCount"]
        clubsGoalDiff = scrapedData["clubsGoalDiff"]
        clubsPoints = scrapedData["clubsPoints"]

        # set the column of titles
        for i in range(5):
            self.label[i] = QLabel(Form)
            if i == 0:
                self.label[0].setGeometry(QRect(80, 145, 20, 20))
                self.label[0].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">Pos</span></p></body></html>"))
            elif i == 1:
                self.label[1].setGeometry(QRect(170, 145, 30, 20))
                self.label[1].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">Club</span></p></body></html>"))
            elif i == 2:
                self.label[2].setGeometry(QRect(320, 145, 20, 20))
                self.label[2].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">Pl</span></p></body></html>"))
            elif i == 3:
                self.label[3].setGeometry(QRect(410, 145, 20, 20))
                self.label[3].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">GD</span></p></body></html>"))
            else:
                self.label[4].setGeometry(QRect(500, 145, 20, 20))
                self.label[4].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">Pts</span></p></body></html>"))

        # set the column of clubs logo (20*20)
        for i in range(5, 25):
            url = clubsLogoLink[i-5]
            image = QImage()
            image.loadFromData(requests.get(url).content)
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(150, 175 + 23*(i-5), 20, 20))
            self.label[i].setPixmap(QPixmap(image))

        # set the column of clubs position
        for i in range(25, 45):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(80, 175 + 23*(i-25), 20, 20))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">%d</span></p></body></html>" %(i-24)))

        # set the column of clubs name
        for i in range(45, 65):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(190, 175 + 23*(i-45), 80, 20))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %clubsName[i-45]))
            if self.favoriteClub == clubsName[i-45]:
                temp = i - 45

        # set the column of clubs matches count
        for i in range(65, 85):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(320, 175 + 23*(i-65), 20, 20))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %clubsMatchesCount[i-65]))

        # set the column of clubs goal difference
        for i in range(85, 105):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(410, 175 + 23*(i-85), 25, 20))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %clubsGoalDiff[i-85]))

        # set the column of clubs points
        for i in range(105, 125):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(500, 175 + 23*(i-105), 20, 20))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %clubsPoints[i-105]))

        # set the triangle sign for the user who know rank of his/her favorite club
        greenTriangleUrl = "https://i.postimg.cc/MHsjVxR5/green-triangle.png"
        greenTriangleImg = QImage()
        greenTriangleImg.loadFromData(requests.get(greenTriangleUrl).content)
        self.label[125] = QLabel(Form)
        self.label[125].setGeometry(QRect(50, 175 + temp*23, 20, 20))
        self.label[125].setPixmap(QPixmap(greenTriangleImg))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[126] = ClickableLabels(Form)
        self.label[126].setGeometry(QRect(5, 5, 30, 30))
        self.label[126].setPixmap(QPixmap(backArrowImg))
        self.label[126].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[126].clicked.connect(lambda: self.back())

        # set the horizpntal line
        self.line = QFrame(Form)
        self.line.setGeometry(QRect(50, 165, 500, 10))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

    # scrape method that does scrape operation and returns clubs data related to standings
    def scrape(self):

        # connect to page of Premier League for get the data and see it as html form
        page = requests.get("https://www.premierleague.com/matchweek/6662/table")
        soup = BeautifulSoup(page.content, "html.parser")

        # get the clubs data
        dataList = [None]*100
        dataList = soup.select("td")

        # get the clubs name
        clubsName = [dataList[i].getText().strip() for i in range(100) if i%5 == 1]

        # get the clubs matches count
        clubsMatchesCount = [dataList[i].getText().strip() for i in range(100) if i%5 == 2]

        # get the clubs goal difference
        clubsGoalDiff = [dataList[i].getText().strip() for i in range(100) if i%5 == 3]

        # get the clubs points
        clubsPoints = [dataList[i].getText().strip() for i in range(100) if i%5 == 4]

        # get the clubs logo link (20*20)
        clubsLogoLink = soup.findAll("img", {"class": "badge-image badge-image--20 js-badge-image"})
        clubsLogoLink = [clubsLogoLink[i].get("src") for i in range(20)]

        scrapedData = {
            "clubsLogoLink": clubsLogoLink,
            "clubsName": clubsName,
            "clubsMatchesCount": clubsMatchesCount,
            "clubsGoalDiff": clubsGoalDiff,
            "clubsPoints": clubsPoints
        }

        return scrapedData

    # if the user clicks on Back button, Account window runs
    def back(self):
        executor = Execution(self.mainWindow, "Account")
        executor.execute(userData=self.__userData)