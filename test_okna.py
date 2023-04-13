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
        self.ph = Physics(self.get_mole_count(), self.get_global_speed())
        self.Moles = self.ph.get_moles()
        self.d = Drawer(self.ui.label_painter)
        
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



      
    def set_V(self):
        self.ui.label_v.setText(str(self.get_global_speed()))
        #self.ph.setV(self.ui.speed_slider.value())

    def set_N(self):
        self.ui.label_n.setText(str(self.get_mole_count()))
        self.ph.setMoles(self.get_mole_count())
        self.Moles = self.ph.get_moles()
        self.draw_moles()

    def get_mole_count(self) -> int:
        return self.ui.mole_slider.value()

    def get_global_speed(self) -> float:
        return self.ui.speed_slider.value()

    def draw_moles(self) -> None:
        self.d.clearCanvas()
        for i in range(len(self.Moles)):
            self.d.drawCircle(self.Moles[i].x, self.Moles[i].y, self.Moles[i].r)
        self.d.refresh()
        

def guiMain(args):
    app = QApplication(args)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
