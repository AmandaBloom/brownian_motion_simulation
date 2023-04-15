from window_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor, QImage, QPixmap, QPen, QPainter, QBrush, QCloseEvent
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QTime
from Drawer import Drawer
from Phisics import Physics
import sys

class MainWindow(QMainWindow):
    """
    Initialization
    """
    def __init__(self, parent=None) -> None:
        # Setup
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ph = Physics(self.getMoleCount(), self.getGlobalSpeed())
        self.Moles = self.ph.getMoles()
        self.d = Drawer(self.ui.label_painter)

        # Set App Icon xD
        self.setWindowIcon(QIcon("diglet_logo.png"))

        # Value on lbls and change physics
        self.setV()
        self.setN()

        # Asyncronic connection label <-> slider
        self.ui.mole_slider.valueChanged.connect(self.setN)
        self.ui.speed_slider.valueChanged.connect(self.setV)
        self.ui.ResetButton.clicked.connect(self.reset)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.doLifeCycle)  # execute `do_life_cycle`
        self.timer.setInterval(10)  # 1000 = 1s
        self.timer.start()
        
        # Init Life
        self.setV()

        self.ui.mole_slider.valueChanged.disconnect()
        self.ui.speed_slider.valueChanged.disconnect()
        self.ui.ResetButton.clicked.disconnect()
    
    def setV(self) -> None:
        self.ui.label_v.setText(str(self.getGlobalSpeed()))
        self.ph.setGlobalSpeed(self.getGlobalSpeed())
        self.ph.setMolesSpeed()
        self.drawMoles()

    def setN(self) -> None:
        self.ui.label_n.setText(str(self.getMoleCount()))
        self.ph.setMoleCount(self.getMoleCount())
        self.Moles = self.ph.getMoles()
        self.drawMoles()

    def getMoleCount(self) -> int:
        return self.ui.mole_slider.value()

    def getGlobalSpeed(self) -> float:
        return self.ui.speed_slider.value()

    def drawMoles(self) -> None:
        self.d.clearCanvas()
        for i in range(len(self.Moles)):
            self.d.drawCircle(self.Moles[i].x, self.Moles[i].y, self.Moles[i].r, QBrush(Qt.red))
        
    def doLifeCycle(self) -> None:
        self.ph.moveMoles()
        self.setN()

    def reset(self) -> None:
        self.ph.delMoles(self.getMoleCount())
        self.ph.addMoles(self.getMoleCount())
        self.ui.ResetButton.setEnabled(False)
        QTimer.singleShot(500, lambda: self.ui.ResetButton.setEnabled(True))

    def closeEvent(self, a0: QCloseEvent) -> None:
        # something is not yes here
        self.timer.stop()
        return super().closeEvent(a0)
        

def guiMain(args):
    app = QApplication(args)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
