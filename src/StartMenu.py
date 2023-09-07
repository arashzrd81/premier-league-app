import sys
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QCoreApplication, QRect, Qt
from PyQt5.QtWidgets import QApplication, QFrame, QLabel
from Execution import Execution
from MainWindow import MainWindow
from ClickableLabels import ClickableLabels



# StartMenu class
class StartMenu():

    # constructor
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.label = [None]*4
        self.line = [None]*2
        self.translate = QCoreApplication.translate

    # setupUi method that performs graphics operations
    def setupUi(self, Form):

        # set the Welcome... text
        self.label[0] = QLabel(Form)
        self.label[0].setGeometry(QRect(70, 220, 450, 60))
        self.label[0].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">Welcome To Premier League App</span></p></body></html>"))

        # set the items (Sign Up, Sign In and Quit)
        for i in range(1, 4):
            self.label[i] = ClickableLabels(Form)
            self.label[i].setGeometry(QRect(180, 350 + 90*(i-1), 230, 60))
            self.label[i].setCursor(QCursor(Qt.PointingHandCursor))
            self.label[i].setStyleSheet("QLabel::hover {background-color: #ff2883;}")
            if i == 1:
                self.label[1].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#ffffff;\">Sign Up</span></p></body></html>"))
                self.label[1].clicked.connect(lambda: self.signUp())
            elif i == 2:
                self.label[2].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#ffffff;\">Sign In</span></p></body></html>"))
                self.label[2].clicked.connect(lambda: self.signIn())
            else:
                self.label[3].setText(self.translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#ffffff;\">Quit</span></p></body></html>"))
                self.label[3].clicked.connect(lambda: self.quitApp())

        # set the horizpntal lines
        for i in range(2):
            self.line[i] = QFrame(Form)
            self.line[i].setGeometry(QRect(160, 423 + i*90, 270, 5))
            self.line[i].setFrameShape(QFrame.HLine)
            self.line[i].setFrameShadow(QFrame.Sunken)

    # if the user clicks on Sign Up button, SignUp window runs
    def signUp(self):
        executor = Execution(self.mainWindow, "SignUp")
        executor.execute()

    # if the user clicks on Sign In button, SignIn window runs
    def signIn(self):
        executor = Execution(self.mainWindow, "SignIn")
        executor.execute()

    # if the user clicks on Quit button, the app closes
    def quitApp(self):
        sys.exit()



# start running the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()