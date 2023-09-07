from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal



# ClickableLabels class
class ClickableLabels(QLabel):

    # attribute
    clicked = pyqtSignal()

    # clickable label operation
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()