from PyQt5.QtWidgets import QWidget
from Error import Error



# Execution class
class Execution():

    # constructor
    def __init__(self, mainWindow, windowName):
        self.mainWindow = mainWindow
        self.windowName = windowName

    # execute method that executed windows
    def execute(self, **kwargs):
        Form = QWidget()

        try:
            # if StartMneu window should be executed
            if self.windowName == "StartMenu":
                from StartMenu import StartMenu
                obj = StartMenu(self.mainWindow)

            # if SignUp window should be executed
            elif self.windowName == "SignUp":
                from SignUp import SignUp
                obj = SignUp(self.mainWindow)

            # if SignIn window should be executed
            elif self.windowName == "SignIn":
                from SignIn import SignIn
                obj = SignIn(self.mainWindow)

            # if Verification window should be executed
            elif self.windowName == "Verification":
                from Verification import Verification
                obj = Verification(self.mainWindow, kwargs["verifyCode"], kwargs["userData"])

            # if Clubs window should be executed
            elif self.windowName == "Clubs":
                from Clubs import Clubs
                obj = Clubs(self.mainWindow, kwargs["userData"])

            # if Account window should be executed
            elif self.windowName == "Account":
                from Account import Account
                obj = Account(self.mainWindow, kwargs["userData"])

            # if AccountSettings window should be executed
            elif self.windowName == "AccountSettings":
                from AccountSettings import AccountSettings
                obj = AccountSettings(self.mainWindow, kwargs["userData"])

            # if Standings window should be executed
            elif self.windowName == "Standings":
                from Standings import Standings
                obj = Standings(self.mainWindow, kwargs["userData"])

            # if Players window should be executed
            elif self.windowName == "Players":
                from Players import Players
                obj = Players(self.mainWindow, kwargs["userData"])

            # if ThePlayer window should be executed
            elif self.windowName == "ThePlayer":
                from ThePlayer import ThePlayer
                obj = ThePlayer(
                        self.mainWindow,
                        kwargs["userData"],
                        kwargs["playerName"],
                        kwargs["clubLogoLink"],
                        kwargs["clubPlayersPageLink"]
                    )

            # if Fixture window should be executed
            elif self.windowName == "Fixture":
                from Fixture import Fixture
                obj = Fixture(self.mainWindow, kwargs["userData"])

            # if Stats window should be executed
            else:
                from Stats import Stats
                obj = Stats(self.mainWindow, kwargs["userData"])

            # set the widget
            obj.setupUi(Form)
            self.mainWindow.addWidget(Form)
            self.mainWindow.setCurrentWidget(Form)

        except: # if an unexpexted error occurred
            obj = Error()
            obj.showError()