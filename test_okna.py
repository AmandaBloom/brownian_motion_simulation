from window_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor, QImage, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QObject, QAbstractTableModel, QSize
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_labelV()
        icon = QIcon()
        icon.addFile(u"diglet_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

    def setup_labelV(self):
        self.ui.label_v.setText("21.37")



def guiMain(args):
    app = QApplication(args)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
