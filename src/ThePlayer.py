import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QCursor, QImage, QPixmap
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from Execution import Execution
from ClickableLabels import ClickableLabels



# ThePlayer class
class ThePlayer():

   # constructor
    def __init__(self, mainWindow, userData, playerName, clubLogoLink, clubPlayersPageLink):
        self.mainWindow = mainWindow
        self.__userData = userData
        self.playerName = playerName
        self.clubLogoLink = clubLogoLink
        self.clubPlayersPageLink = clubPlayersPageLink
        self.label = [None]*34
        self.line = [None]*18
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # get the persoanl data and technical data of the player
        personalData, technicalData = self.scrape()

        # set the white square for background of the club logo
        whitePageUrl = "https://i.postimg.cc/vBJQH96K/white-page.png"
        whitePageImg = QImage()
        whitePageImg.loadFromData(requests.get(whitePageUrl).content)
        self.label[2] = QLabel(Form)
        self.label[2].setGeometry(QRect(320, 180, 60, 60))
        self.label[2].setPixmap(QPixmap(whitePageImg))

        # set the logo of club (50*50) on the top
        clubLogoUrl = self.clubLogoLink
        clubLogoImg = QImage()
        clubLogoImg.loadFromData(requests.get(clubLogoUrl).content)
        self.label[3] = QLabel(Form)
        self.label[3].setGeometry(QRect(325, 185, 50, 50))
        self.label[3].setPixmap(QPixmap(clubLogoImg))

        # set the pink rectangle for background of the player name
        pinkRectangleUrl = "https://i.postimg.cc/g07RJvXV/pink-rectangle.png"
        pinkRectangleImg = QImage()
        pinkRectangleImg.loadFromData(requests.get(pinkRectangleUrl).content)
        self.label[4] = QLabel(Form)
        self.label[4].setGeometry(QRect(380, 180, 200, 60))
        self.label[4].setPixmap(QPixmap(pinkRectangleImg))

        # set the name of the player on the top
        self.label[5] = QLabel(Form)
        self.label[5].setGeometry(QRect(395, 200, 300, 20))
        self.label[5].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %self.playerName))

        # set the player image
        playerImgUrl = personalData[0]
        playerImg = QImage()
        playerImg.loadFromData(requests.get(playerImgUrl).content)
        self.label[6] = QLabel(Form)
        self.label[6].setGeometry(QRect(35, 155, 220, 270))
        self.label[6].setPixmap(QPixmap(playerImg))

        # set the Individual Features text (in light green rectangle)
        url = "https://i.postimg.cc/T3FsycxC/individual-features-title.png"
        img = QImage()
        img.loadFromData(requests.get(url).content)
        self.label[7] = QLabel(Form)
        self.label[7].setGeometry(QRect(15, 434, 264, 35))
        self.label[7].setPixmap(QPixmap(img))

        # set the fixed items of Individual Features
        personalFixedItems = ["Position", "Nationality", "Age", "Height"]
        for i in range(8, 12):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(25, 481 + 45*(i-8), 90, 25))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %personalFixedItems[i-8]))

        # set the modifiable items of Individual Features
        for i in range(12, 16):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(100, 481 + 45*(i-12), 170, 25))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"right\"><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %personalData[i-11]))

        # set the Individual Statistics text (in light green rectangle)
        url = "https://i.postimg.cc/T31w2T2n/individual-statistics-title.png"
        img = QImage()
        img.loadFromData(requests.get(url).content)
        self.label[16] = QLabel(Form)
        self.label[16].setGeometry(QRect(320, 255, 264, 35))
        self.label[16].setPixmap(QPixmap(img))

        # set the first series of Individual Statistics fixed items
        technicalFixedItems = ["Appearances", "Goals"]
        for i in range(17, 19):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(327, 300 + 45*(i-17), 160, 25))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %technicalFixedItems[i-17]))

        # set the second series of Individual Statistics fixed items
        goalkeepersFixedItems = ["Clean Sheets", "Saves", "Penalties Saves", "Goals Conceded", "Yellow Cards", "Red Cards"]
        defendersFixedItems = ["Tackles Success %", "Duel Won %", "Aerial Battles Won %", "Assists", "Yellow Cards", "Red Cards"]
        midfieldersFixedItems = ["Big Chances Created", "Assists", "Duel Won %", "Cross Accuracy %", "Yellow Cards", "Red Cards"]
        forwardFixedItems = ["Goals Per Match", "Shoot Accuracy", "Assists", "Headed Goals", "Yellow Cards", "Red Cards"]

        # according to the player position, should display individual statistics for that position
        for i in range(19, 25):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(327, 300 + 45*(i-17), 160, 25))

        # if the player was a goalkeeper, should have to display the individual statistics of the goalkeepers
        if personalData[1] == "Goalkeeper":
            for i in range(19, 25):
                self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %goalkeepersFixedItems[i-19]))

        # if the player was a defender, should have to display the individual statistics of the defenders
        elif personalData[1] == "Defender":
            for i in range(19, 25):
                self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %defendersFixedItems[i-19]))

        # if the player was a midfielder, should have to display the individual statistics of the midfielders
        elif personalData[1] == "Midfielder":
            for i in range(19, 25):
                self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %midfieldersFixedItems[i-19]))

        # if the player was a forward, should have to display the individual statistics of the forwards
        else:
            for i in range(19, 25):
                self.label[i].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %forwardFixedItems[i-19]))

        # set the modifiable items of Individual Statistics
        for i in range(25, 33):
            self.label[i] = QLabel(Form)
            self.label[i].setGeometry(QRect(515, 300 + 45*(i-25), 60, 25))
            self.label[i].setText(self.translate("Form", "<html><head/><body><p align=\"right\"><span style=\" font-size:11pt; font-weight:600; color:#ffffff;\">%s</span></p></body></html>" %technicalData[i-25]))

        # set the back arrow sign
        backArrowUrl = "https://i.postimg.cc/qqp5gcXn/back-arrow.png"
        backArrowImg = QImage()
        backArrowImg.loadFromData(requests.get(backArrowUrl).content)
        self.label[33] = ClickableLabels(Form)
        self.label[33].setGeometry(QRect(5, 5, 30, 30))
        self.label[33].setPixmap(QPixmap(backArrowImg))
        self.label[33].setCursor(QCursor(Qt.PointingHandCursor))
        self.label[33].clicked.connect(lambda: self.back())

        # set the horizontal lines of Individual Features table
        for i in range(5):
            self.line[i] = QFrame(Form)
            self.line[i].setGeometry(QRect(15, 468 + i*45, 264, 5))
            self.line[i].setFrameShape(QFrame.HLine)
            self.line[i].setFrameShadow(QFrame.Sunken)

        # set the vertical lines of Individual Features table
        for i in range(5, 7):
            self.line[i] = QFrame(Form)
            self.line[i].setGeometry(QRect(14 + 262*(i-5), 471, 5, 181))
            self.line[i].setFrameShape(QFrame.VLine)
            self.line[i].setFrameShadow(QFrame.Sunken)

        # set the horizontal lines of Individual Statistics table
        for i in range(7, 16):
            self.line[i] = QFrame(Form)
            self.line[i].setGeometry(QRect(320, 288 + 45*(i-7), 264, 5))
            self.line[i].setFrameShape(QFrame.HLine)
            self.line[i].setFrameShadow(QFrame.Sunken)

        # set the vertical lines of Individual Statistics table
        for i in range(16, 18):
            self.line[i] = QFrame(Form)
            self.line[i].setGeometry(QRect(319 + 262*(i-16), 290, 5, 361))
            self.line[i].setFrameShape(QFrame.VLine)
            self.line[i].setFrameShadow(QFrame.Sunken)

    # scrape method that does scrape operation and returns the player data
    def scrape(self):

        # connect to page of club players that the user is in favor of and see it as html form
        page = requests.get(self.clubPlayersPageLink)
        soup = BeautifulSoup(page.content, "html.parser")

        # obtain the player page link
        playersPagesLinks = soup.findAll('a', {"class": "playerOverviewCard active"})
        thePlayerPageLink = ''.join(["https://www.premierleague.com" + playersPagesLinks[i].get("href") for i in range(len(playersPagesLinks)) if self.playerName.replace(' ', '-') in playersPagesLinks[i].get("href")])

        # obtain the player image link
        playersImagesLinks = soup.findAll("img", {"class": "img statCardImg"})
        theplayerImageLink = ''.join(["https://resources.premierleague.com/premierleague/photos/players/110x140/" + playersImagesLinks[i].get("data-player") + ".png" for i in range(len(playersImagesLinks)) if self.playerName.replace(' ', '-') in playersPagesLinks[i].get("href")])
        if requests.get(theplayerImageLink).status_code != 200:
            theplayerImageLink = "https://resources.premierleague.com/premierleague/photos/players/110x140/Photo-Missing.png"

        # connect to first tab of the player page for get the data about the player
        page = requests.get(thePlayerPageLink)
        soup = BeautifulSoup(page.content, "html.parser")

        # get the general data
        Generaldata = soup.findAll("div", {"class": "info"})[1:5]

        # set the player data one by one
        personalData = []
        personalData.append(theplayerImageLink)
        personalData.extend([Generaldata[i].getText().strip() if i != 2 else Generaldata[i].getText().strip()[12:14] for i in range(4)])

        # connect to second tab of the player page for get the data about the player
        page = requests.get(thePlayerPageLink.replace("overview", "stats?co=1&se=418"))
        soup = BeautifulSoup(page.content, "html.parser")

        # get the shared data between all players with each position in last season of Premier League
        appearances = soup.find("span", {"class": "allStatContainer statappearances", "data-stat": "appearances"}).getText().strip()
        goals = soup.find("span", {"class": "allStatContainer statgoals", "data-stat": "goals"}).getText().strip()
        yellowCards = soup.find("span", {"class": "allStatContainer statyellow_card", "data-stat": "yellow_card"}).getText().strip()
        redCards = soup.find("span", {"class": "allStatContainer statred_card", "data-stat": "red_card"}).getText().strip()
        technicalData = [appearances, goals]

        # get the data related to goalkeepers
        if personalData[1] == "Goalkeeper":
            cleanSheets = soup.find("span", {"class": "allStatContainer statclean_sheet", "data-stat": "clean_sheet"}).getText().strip()
            saves = soup.find("span", {"class": "allStatContainer statsaves", "data-stat": "saves"}).getText().strip()
            penaltiesSaves = soup.find("span", {"class": "allStatContainer statpenalty_save", "data-stat": "penalty_save"}).getText().strip()
            goalsConceded = soup.find("span", {"class": "allStatContainer statgoals_conceded", "data-stat": "goals_conceded"}).getText().strip()
            technicalData.extend([cleanSheets, saves, penaltiesSaves, goalsConceded, yellowCards, redCards])

        # if the player position was not goalkeeper
        else:
            # get the player count of assists in the last season of Premier League
            assists = soup.find("span", {"class": "allStatContainer statgoal_assist", "data-stat": "goal_assist"}).getText().strip()

            # get the data related to defenders and midfielders
            if (personalData[1] == "Defender") or (personalData[1] == "Midfielder"):

                # get the player percentage success in duels
                duelsWon = int(soup.find("span", {"class": "allStatContainer statduel_won", "data-stat": "duel_won"}).getText().strip().replace(',', ''))
                duelLost = int(soup.find("span", {"class": "allStatContainer statduel_lost", "data-stat": "duel_lost"}).getText().strip().replace(',', ''))
                if duelsWon + duelLost == 0:
                    duelsWonPercent = "__"
                else:
                    duelsWonPercent = str(round(duelsWon * 100 / (duelsWon + duelLost), 1)) + '%'

                # get the data related to defenders
                if personalData[1] == "Defender":
                    tacklesSuccessPercent = soup.find("span", {"class": "allStatContainer stattackle_success", "data-stat": "won_tackle", "data-denominator": "total_tackle", "data-percent": "true"}).getText().strip()
                    aerialBattlesWon = int(soup.find("span", {"class": "allStatContainer stataerial_won", "data-stat": "aerial_won"}).getText().strip().replace(',', ''))
                    aerialBattlesLost = int(soup.find("span", {"class": "allStatContainer stataerial_lost", "data-stat": "aerial_lost"}).getText().strip().replace(',', ''))
                    if aerialBattlesWon + aerialBattlesLost == 0:
                        aerialBattlesWonPercent = "__"
                    else:
                        aerialBattlesWonPercent = str(round(aerialBattlesWon * 100 / (aerialBattlesWon + aerialBattlesLost), 1)) + '%'
                    technicalData.extend([tacklesSuccessPercent, duelsWonPercent, aerialBattlesWonPercent, assists, yellowCards, redCards])

                # get the data related to midfielders
                else:
                    crossAccuracy = soup.find("span", {"class": "allStatContainer statcross_accuracy", "data-stat": "accurate_cross", "data-denominator": "total_cross", "data-percent": "true"}).getText().strip()
                    bigChancesCreated = soup.find("span", {"class": "allStatContainer statbig_chance_created", "data-stat": "big_chance_created"}).getText().strip()
                    technicalData.extend([bigChancesCreated, assists, duelsWonPercent, crossAccuracy, yellowCards, redCards])

            # get the data related to forwards
            else:
                goalsPerMatch = soup.find("span", {"class": "allStatContainer statgoals_per_game", "data-stat": "goals", "data-denominator": "appearances"}).getText().strip()
                shootAccuracy = soup.find("span", {"class": "allStatContainer statshot_accuracy", "data-stat": "ontarget_scoring_att", "data-denominator": "total_scoring_att", "data-percent": "true"}).getText().strip()
                headedGoals = soup.find("span", {"class": "allStatContainer statatt_hd_goal", "data-stat": "att_hd_goal"}).getText().strip()
                technicalData.extend([goalsPerMatch, shootAccuracy, assists, headedGoals, yellowCards, redCards])

        return personalData, technicalData

    # if the user clicks on Back button, Players window runs
    def back(self):
        executor = Execution(self.mainWindow, "Players")
        executor.execute(userData=self.__userData)