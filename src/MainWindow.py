import requests
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QStackedWidget
from Error import Error
from Execution import Execution



# MainWindow class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self):
        super().__init__()

        # set the main window
        self.mainWindow = QStackedWidget()
        self.setCentralWidget(self.mainWindow)
        self.setWindowTitle("Premier League App")
        self.setGeometry(QRect(370, 40, 600, 670))

        try:
            # set the icon of the window bar
            url = "https://i.postimg.cc/C1XY0nG0/lion.png"
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(url).content)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

            # set the purple theme (background)
            url = "https://i.postimg.cc/mkVxmdbm/purple-theme.png"
            img = QImage()
            img.loadFromData(requests.get(url).content)
            label_1 = QLabel(self.mainWindow)
            label_1.setGeometry(QRect(0, 0, 600, 670))
            label_1.setPixmap(QPixmap(img))

            # set the logo and text of Premier League on the top of the window
            url = "https://i.postimg.cc/htWFpqrC/logo.png"
            img = QImage()
            img.loadFromData(requests.get(url).content)
            label_2 = QLabel(self.mainWindow)
            label_2.setGeometry(QRect(47, 27, 500, 110))
            label_2.setPixmap(QPixmap(img))

            # execute StartMenu window
            executor = Execution(self.mainWindow, "StartMenu")
            executor.execute()

        except:
            obj = Error()
            obj.showError()