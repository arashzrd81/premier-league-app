import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Execution import Execution
from ClickableLabels import ClickableLabels



# Stats class
class Stats():

    # constructor
    def __init__(self, mainWindow, userData):
        self.mainWindow = mainWindow
        self.__userData = userData
        self.favoriteClub = self.__userData["favoriteClub"]
        self.label = [None]*61
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # get the club logo link and clubs statistics
        clubLogoLink, statistics = self.scrape()

        # set the white square for background of the club logo
        whitePageUrl = "https://i.postimg.cc/vBJQH96K/white-page.png"
        whitePageImg = QImage()
        whitePageImg.loadFromData(requests.get(whitePageUrl).content)
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(50, 160, 60, 60))
        self.label[0].setPixmap(QPixmap(whitePageImg))

        # set the logo of club (50*50) on the top
        clubLogoUrl = clubLogoLink
        clubLogoImg = QImage()
        clubLogoImg.loadFromData(requests.get(clubLogoUrl).content)
        self.label[1] = QLabel(Form)
        self.label[1].setGeometry(QRect(55, 165, 50, 50))
        self.label[1].setPixmap(QPixmap(clubLogoImg))

        # set the pink rectangle for background of the club name
        pinkRectangleUrl = "https://i.postimg.cc/fThpk9fB/pink-rectangle.png"
        pinkRectangleImg = QImage()
        pinkRectangleImg.loadFromData(requests.get(pinkRectangleUrl).content)
        self.label[2] = QLabel(Form)
        self.label[2].setGeometry(QRect(110, 160, 200, 60))
        self.label[2].setPixmap(QPixmap(pinkRectangleImg))

        # set the name of club on the top
        self.label[3] = QLabel(Form)
        self.label[3].setGeometry(QRect(120, 180, 200, 20))
        self.label[3].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">%s Stats</span></p></body></html>" %self.favoriteClub))

        # set the white rectangles for background of items
        for i in range(4, 18):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(50, 240 + 30*(i-4), 250, 25))
            self.label[i].setPixmap(QPixmap(whitePageImg))

        # set the pink rectangles for background of items
        for i in range(18, 32):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(300, 240 + 30*(i-18), 250, 25))
            self.label[i].setPixmap(QPixmap(pinkRectangleImg))

        # set the fixed items
        fixedItems = [
            "Matches Played",
            "Wins",
            "Losses",
            "Goals Scored",
            "Goals Scored Per Match",
            "Golas Conceded",
            "Goals Conceded Per Match",
            "Clean Sheets",
            "Penalties Scored",
            "Big Chances Created",
            "Passes Per Match",
            "Error Leading To Goal",
            "Yellow Cards",
            "Red Cards"
        ]
        for i in range(32, 46):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(60, 242 + 30*(i-32), 230, 20))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#000000;\">%s</span></p></body></html>" %fixedItems[i-32]))

        # set the statistics
        for i in range(46, 60):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(310, 242 + 30*(i-46), 230, 20))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %statistics[i-46]))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[60] = ClickableLabels(Form)
        self.label[60].setGeometry(QRect(5, 5, 30, 30))
        self.label[60].setPixmap(QPixmap(backArrowImg))
        self.label[60].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[60].clicked.connect(lambda: self.back())

    # scrape method that does scrape operation and returns clubs name and clubs logo link (25*25) and dates
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
        clubLogoLink = ''.join([clubsLogoLink[i].get("src").replace("/20", "/50") for i in range(20) if self.favoriteClub in clubsName[i]])

        # obtain stats pages link and find the favorite club stats page link
        data = soup.select('a')
        clubsStatsPagesLink = data[133:153]
        clubStatsPageLink = ''.join(["https://www.premierleague.com" + clubsStatsPagesLink[i].get("href").replace("overview", "stats") for i in range(20) if self.favoriteClub in clubsName[i]])

        # connect to page of club stats that the user is in favor of and see it as html form
        page = requests.get(clubStatsPageLink)
        soup = BeautifulSoup(page.content, "html.parser")

        # get the count of matches played of the club
        matchesPlayed = soup.find("span", {"class": "allStatContainer statmatches_played", "data-stat": "wins,draws,losses"})

        # get the count of matches that the club wins in them
        wins = soup.find("span", {"class": "allStatContainer statwins", "data-stat": "wins"})

        # get the count of matches that the club losses in them
        losses = soup.find("span", {"class": "allStatContainer statlosses", "data-stat": "losses"})

        # get the count of goals scored by the club
        goalsScored = soup.find("span", {"class": "allStatContainer statgoals", "data-stat": "goals"})

        # get the goals scored per match of the club
        goalsScoredPerMatch = soup.find("span", {"class": "allStatContainer statgoals_per_game", "data-stat": "goals", "data-denominator": "wins,draws,losses"})

        # get the count of goals conceded by the club
        golasConceded = soup.find("span", {"class": "allStatContainer statgoals_conceded", "data-stat": "goals_conceded"})

        # get the goals conceded per match of the club
        goalsConcededPerMatch = soup.find("span", {"class": "allStatContainer statgoals_conceded_per_game", "data-stat": "goals_conceded", "data-denominator": "wins,draws,losses"})

        # get the count of clean sheets by the club
        cleanSheets = soup.find("span", {"class": "allStatContainer statclean_sheet", "data-stat": "clean_sheet"})

        # get the count of penalties scored by the club
        penaltiesScored = soup.find("span", {"class": "allStatContainer statatt_pen_goal", "data-stat": "att_pen_goal"})

        # get the big chances created by the club
        bigChancesCreated = soup.find("span", {"class": "allStatContainer statbig_chance_created", "data-stat": "big_chance_created"})

        # get the passes per match of the club
        passesPerMatch = soup.find("span", {"class": "allStatContainer stattotal_pass_per_game", "data-stat": "total_pass", "data-denominator": "wins,draws,losses"})

        # get the error leading to goal of the club
        errorLeadingToGoal = soup.find("span", {"class": "allStatContainer staterror_lead_to_goal", "data-stat": "error_lead_to_goal"})

        # get the yellow cards those receive by the club
        yellowCards = soup.find("span", {"class": "allStatContainer statyellow_card", "data-stat": "total_yel_card"})

        # get the red cards those receive by the club
        redCards = soup.find("span", {"class": "allStatContainer statred_card", "data-stat": "total_red_card"})

        # extend the items to a list and get their main text
        statistics = [
            matchesPlayed,
            wins,
            losses,
            goalsScored,
            goalsScoredPerMatch,
            golasConceded,
            goalsConcededPerMatch,
            cleanSheets,
            penaltiesScored,
            bigChancesCreated,
            passesPerMatch,
            errorLeadingToGoal,
            yellowCards,
            redCards
        ]
        statistics = [statistics[i].getText().strip() for i in range(14)]

        return clubLogoLink, statistics

    # if the user clicks on Back button, Account window runs
    def back(self):
        executor = Execution(self.mainWindow, "Account")
        executor.execute(userData=self.__userData)