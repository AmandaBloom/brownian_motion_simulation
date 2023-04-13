from window_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor, QImage, QPixmap, QPen, QPainter
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QObject, QAbstractTableModel, QSize
from Drawer import Drawer
from Phisics import Physics, Mole
import sys
import os

class MainWindow(QMainWindow):
    """
    Initialization
    """
    def __init__(self, parent=None) -> None:
        # Setup
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Labels initialization
        self.set_V()
        self.set_N()

        # Asyncronic connection label <-> slider
        self.ui.mole_slider.valueChanged.connect(self.set_N)
        self.ui.speed_slider.valueChanged.connect(self.set_V)

        # Set App Icon xD
        icon = QIcon()
        icon.addFile(u"diglet_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        ph = Physics(self.get_mole_count(), self.get_global_speed())
        Moles = ph.get_moles()

        d = Drawer(self.ui.label_painter)
        for i in range(len(Moles)):
            d.drawCircle(Moles[i].x, Moles[i].y, Moles[i].r)
        

        # d = Drawer(self.ui.label_painter)
        # d.drawCircle(100, 100, 3)
        # d.drawCircle(120, 100, 3)
        #d.clearCanvas()
      
    def set_V(self):
        self.ui.label_v.setText(str(self.get_global_speed()))
        #self.ph.setV(self.ui.speed_slider.value())

    def set_N(self):
        self.ui.label_n.setText(str(self.get_mole_count()))
        #self.ph.setN(self.ui.mole_slider.value())

    def get_mole_count(self) -> int:
        return self.ui.mole_slider.value()

    def get_global_speed(self) -> float:
        return self.ui.speed_slider.value()


def guiMain(args):
    app = QApplication(args)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
