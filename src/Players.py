import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Execution import Execution
from ClickableLabels import ClickableLabels



# Players class
class Players(QWidget):

    # constructor
    def __init__(self, mainWindow, userData):
        super().__init__()
        self.mainWindow = mainWindow
        self.__userData = userData
        self.favoriteClub = self.__userData["favoriteClub"]
        self.label = [None]*58
        self.translate = QCoreApplication.translate
        self.playerName = None
        self.clubLogoLink = None
        self.clubPlayersPageLink = None

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # get the club logo link (50*50) and players name
        goalkeepers, defenders, midfielders, forwards = self.scrape()

        # get the count of players in each position
        lg = len(goalkeepers)
        ld = len(defenders)
        lm = len(midfielders)
        lf = len(forwards)

        # set the white square for background of the club logo
        whitePageUrl = "https://i.postimg.cc/vBJQH96K/white-page.png"
        whitePageImg = QImage()
        whitePageImg.loadFromData(requests.get(whitePageUrl).content)
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(10, 150, 60, 60))
        self.label[0].setPixmap(QPixmap(whitePageImg))

        # set the logo of club (50*50) on the top
        clubLogoUrl = self.clubLogoLink
        clubLogoImg = QImage()
        clubLogoImg.loadFromData(requests.get(clubLogoUrl).content)
        self.label[1] = QLabel(Form)
        self.label[1].setGeometry(QRect(15, 155, 50, 50))
        self.label[1].setPixmap(QPixmap(clubLogoImg))

        # set the pink rectangle for background of the club name
        pinkRectangleUrl = "https://i.postimg.cc/fThpk9fB/pink-rectangle.png"
        pinkRectangleImg = QImage()
        pinkRectangleImg.loadFromData(requests.get(pinkRectangleUrl).content)
        self.label[2] = QLabel(Form)
        self.label[2].setGeometry(QRect(70, 150, 200, 60))
        self.label[2].setPixmap(QPixmap(pinkRectangleImg))

        # set the name of club on the top
        self.label[3] = QLabel(Form)
        self.label[3].setGeometry(QRect(80, 170, 200, 20))
        self.label[3].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">%s Players</span></p></body></html>" %self.favoriteClub))

        # set the place of players names (clickable) and position titles
        for i in range(4, lf+lm+ld+lg+11):
            if (5 <= i <= lg+4) or (lg+7 <= i <= ld+lg+6) or (ld+lg+9 <= i <= lm+ld+lg+8) or (lm+ld+lg+11 <= i <= lf+lm+ld+lg+10):
                self.label[i] = ClickableLabels(Form)
                self.label[i].setCursor(QCursor(Qt.PointingHandCursor))
                self.label[i].setStyleSheet("QLabel::hover {background-color: #ff2883;}")
            else:
                self.label[i] = QLabel(Form)

            if 4 <= i <= 16:
                self.label[i].setGeometry(QRect(10, 230 + 33*(i-4), 140, 30))
            elif 17 <= i <= 29:
                self.label[i].setGeometry(QRect(160, 230 + 33*(i-17), 140, 30))
            elif 30 <= i <= 42:
                self.label[i].setGeometry(QRect(310, 230 + 33*(i-30), 140, 30))
            else:
                self.label[i].setGeometry(QRect(460, 230 + 33*(i-43), 140, 30))

        # create an object from QImage to set the pink rectangles
        img = QImage()

        # set the Goalkeepers text (in light green rectangle) and players with goalkeeper position and clickable them
        url = "https://i.postimg.cc/G25fdbFD/goalkeepers-title.png"
        img.loadFromData(requests.get(url).content)
        self.label[4].setPixmap(QPixmap(img))
        self.label[lg+5].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:13pt; color:#ffffff;\">.........................</span></p></body></html>"))
        for i in range(5, lg+5):
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; color:#ffffff;\">%s</span></p></body></html>" %goalkeepers[i-5]))
            self.label[i].clicked.connect(lambda: self.thePlayer())

        # set the Defenders text (in light green rectangle) and players with defender position and clickable them
        url = "https://i.postimg.cc/BZdqC0rt/defenders-title.png"
        img.loadFromData(requests.get(url).content)
        self.label[lg+6].setPixmap(QPixmap(img))
        self.label[ld+lg+7].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:13pt; color:#ffffff;\">.........................</span></p></body></html>"))
        for i in range(lg+7, ld+lg+7):
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; color:#ffffff;\">%s</span></p></body></html>" %defenders[i-lg-7]))
            self.label[i].clicked.connect(lambda: self.thePlayer())

        # set the Midfielders text (in light green rectangle) and players with midfielder position and clickable them
        url = "https://i.postimg.cc/Gp7RTwPL/midfielders-title.png"
        img.loadFromData(requests.get(url).content)
        self.label[ld+lg+8].setPixmap(QPixmap(img))
        self.label[lm+ld+lg+9].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:13pt; color:#ffffff;\">.........................</span></p></body></html>"))
        for i in range(ld+lg+9, lm+ld+lg+9):
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; color:#ffffff;\">%s</span></p></body></html>" %midfielders[i-ld-lg-9]))
            self.label[i].clicked.connect(lambda: self.thePlayer())

        # set the Forwards text (in light green rectangle) and players with forward position and clickable them
        url = "https://i.postimg.cc/d01PYHbz/forwards-title.png"
        img.loadFromData(requests.get(url).content)
        self.label[lm+ld+lg+10].setPixmap(QPixmap(img))
        for i in range(lm+ld+lg+11, lf+lm+ld+lg+11):
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; color:#ffffff;\">%s</span></p></body></html>" %forwards[i-lm-ld-lg-11]))
            self.label[i].clicked.connect(lambda: self.thePlayer())

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[lf+lm+ld+lg+11] = ClickableLabels(Form)
        self.label[lf+lm+ld+lg+11].setGeometry(QRect(5, 5, 30, 30))
        self.label[lf+lm+ld+lg+11].setPixmap(QPixmap(backArrowImg))
        self.label[lf+lm+ld+lg+11].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[lf+lm+ld+lg+11].clicked.connect(lambda: self.back())

    # scrape method that does scrape operation and returns club players names
    def scrape(self):

        # connect to page of Premier League for get the data and see it as html form
        page = requests.get("https://www.premierleague.com/matchweek/6662/table")
        soup = BeautifulSoup(page.content, "html.parser")

        # get the clubs name to find the favorite club logo link (50*50)
        dataList = [None]*100
        dataList = soup.select("td")
        clubsName = [dataList[i].getText().strip() for i in range(100) if i%5 == 1]

        # get the clubs logo link and find the favorite club logo link
        clubsLogoLink = soup.findAll("img", {"class": "badge-image badge-image--20 js-badge-image"})
        self.clubLogoLink = ''.join([clubsLogoLink[i].get("src").replace("/20", "/50") for i in range(20) if self.favoriteClub in clubsName[i]])

        # obtain players pages link and find the favorite club stats page link
        data = soup.select('a')
        clubsplayersPagesLink = data[133:153]
        self.clubPlayersPageLink = ''.join(["https://www.premierleague.com" + clubsplayersPagesLink[i].get("href").replace("overview", "squad") for i in range(20) if self.favoriteClub in clubsName[i]])

        # connect to page of club players that the user is in favor of and see it as html form
        page = requests.get(self.clubPlayersPageLink)
        soup = BeautifulSoup(page.content, "html.parser")

        # get the players names
        playersNames = soup.findAll("h4", {"class": "name"})
        playersNames = [playersNames[i].getText() for i in range(len(playersNames))]

        # get the players positions
        playersPositions = soup.findAll("span", {"class": "position"})
        playersPositions = [playersPositions[i].getText() for i in range(len(playersPositions))]

        # putting together the names and positions in tuples within a list
        players = list(zip(playersNames, playersPositions))

        # separate the goalkeepers
        goalkeepers = [player[0] for player in players if player[1] == "Goalkeeper"]

        # separate the defenders
        defenders = [player[0] for player in players if player[1] == "Defender"]

        # separate the midfielders
        midfielders = [player[0] for player in players if player[1] == "Midfielder"]

        # separate the forwards
        forwards = [player[0] for player in players if player[1] == "Forward"]

        return goalkeepers, defenders, midfielders, forwards

    # if the user clicks on a player, ThePlayer window runs
    def thePlayer(self):

        # obtain the player name
        self.playerName = self.sender().text()
        self.playerName = BeautifulSoup(self.playerName, "html.parser").getText()

        # execute ThePlayer window
        executor = Execution(self.mainWindow, "ThePlayer")
        executor.execute(
            userData=self.__userData,
            playerName=self.playerName,
            clubLogoLink=self.clubLogoLink,
            clubPlayersPageLink=self.clubPlayersPageLink
        )

    # if the user clicks on Back button, Account window runs
    def back(self):
        executor = Execution(self.mainWindow, "Account")
        executor.execute(userData=self.__userData)