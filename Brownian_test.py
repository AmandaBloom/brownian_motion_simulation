from window_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import (
    QIcon,
    QColor,
    QImage,
    QPixmap,
    QPen,
    QPainter,
    QBrush,
    QCloseEvent,
)
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QTime
from Drawer import Drawer
from Phisics import Physics, Mole
import sys
import math


class MainWindow(QMainWindow):
    """
    Initialization
    """

    def __init__(self, parent=None) -> None:
        # Setup
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ph = Physics(0, self.getGlobalSpeed())
        self.ph.Moles = [Mole(self.getGlobalSpeed(), 100, 295, 0), Mole(self.getGlobalSpeed(), 600, 305, -1*math.pi)]
        self.Moles = self.ph.getMoles()
        self.d = Drawer(self.ui.label_painter)
        self.colours = [Qt.red, Qt.white, Qt.blue, Qt.yellow, Qt.black,
                        Qt.darkYellow, Qt.green, Qt.magenta, Qt.cyan, Qt.gray]
        self.ui.label_v.setText(str(self.ph.Vol))

        # Set App Icon xD
        self.setWindowIcon(QIcon("diglet_logo.png"))

        # Value on lbls and change physics
        self.setV()

        # Asyncronic connection label <-> slider
        self.ui.speed_slider.valueChanged.connect(self.setV)
        self.ui.ResetButton.clicked.connect(self.reset)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.doLifeCycle)  # execute `do_life_cycle`
        self.timer.setInterval(20)  # 1000 = 1s; 20 = 1/50s
        self.timer.start()

        # Init Life
        
        self.setV()

    def setV(self) -> None:
        self.ph.setGlobalSpeed(self.getGlobalSpeed())
        self.ph.setMolesSpeed()
        self.drawMoles()

    def setVol(self) -> None:
        self.ui.label_v(str(self.ph.Vol))

    def setP(self) -> None:
        pressure = self.ph.wall_momentum
        self.ui.label_p(pressure)

    # def setN(self) -> None:
    #     self.ui.label_n.setText(str(self.getMoleCount()))
    #     self.ph.setMoleCount(self.getMoleCount())
    #     self.Moles = self.ph.getMoles()
    #     self.drawMoles()

    def live(self):
        self.Moles = self.ph.getMoles()
        self.drawMoles()   

    def setP(self) -> None:
        self.ui.label_p.setText(str(self.ph.getWallMomentum()))

    def setNT(self) -> None:
        self.ui.label_kt.setText(str(self.ph.getKT()))

    def getMoleCount(self) -> int:
        return self.ui.mole_slider.value()

    def getGlobalSpeed(self) -> float:
        return self.ui.speed_slider.value()

    def drawMoles(self) -> None:
        self.d.clearCanvas()
        for mole in self.Moles:
            self.d.drawCircle(
                mole.x, mole.y, mole.r, QBrush(self.colours[mole.color_idx])
            )

    def doLifeCycle(self) -> None:
        self.ph.moveMoles()
        self.live()

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
