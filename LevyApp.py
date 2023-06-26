from window_ui1 import Ui_MainWindow
from Drawer import Drawer
from LevyPhisics import LevyPhysics
import sys
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
import threading
import numpy as np


class MainWindow(QMainWindow):
    """
    Initialization
    """

    def __init__(self, parent=None) -> None:
        # Setup
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ph = LevyPhysics()
        self.d = Drawer(self.ui.label_painter)
        self.maxX, self.maxY = 350, 350
        # Set App Icon xD
        self.setWindowIcon(QIcon("plane.png"))
        self.ui.label_alpha.setText(str(self.ph.alpha))
        self.ui.label_stepsize.setText(str(self.ph.stepSize))

        # Value on lbls and change physics
        self.setAlpha()
        self.setStepSize()

        self.lock = threading.Lock()

        # Asyncronic connection label <-> slider
        self.ui.alpha_slider.valueChanged.connect(self.setAlpha)
        self.ui.StepSize_slider.valueChanged.connect(self.setStepSize)
        self.ui.ResetButton.clicked.connect(self.reset)
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.doLifeCycle
        )  # execute `do_life_cycle` (order 66)
        self.timer.setInterval(20)  # 1000 = 1s; 20 = 1/50s
        self.timer.start()

        self.d.clearCanvas()
        self.ph.doIter()

    def setFPS(self) -> None:
        self.ui.label_fps.setText(str(self.ph.getFPS()))

    def getAlpha(self) -> int:
        return self.ui.alpha_slider.value()

    def getStepSize(self) -> int:
        return self.ui.StepSize_slider.value()

    def setAlpha(self) -> None:
        self.ui.label_alpha.setText(str(self.ph.alpha))
        self.ph.setAlpha(self.getAlpha())

    def setStepSize(self) -> None:
        self.ui.label_stepsize.setText(str(self.ph.stepSize))
        self.ph.setStepSize(self.getStepSize())

    def drawLevyTrace(self) -> None:
        pos = self.ph.getLevyPositions()
        self.maxX, self.maxY = max(abs(pos[:, 0] - 350)), max(abs(pos[:, 1] - 350))
        if len(pos) < 2:
            return
        if max(self.maxX, self.maxY) > 350:
            pos[:, 0] = np.interp(
                pos[:, 0], (pos[:, 0].min(), pos[:, 0].max()), (20, 680)
            )
            pos[:, 1] = np.interp(
                pos[:, 1], (pos[:, 1].min(), pos[:, 1].max()), (20, 680)
            )
        else:
            for idx in range(len(pos) - 1):
                self.d.drawLine(
                    round(pos[idx, 0]),
                    round(pos[idx, 1]),
                    round(pos[idx + 1, 0]),
                    round(pos[idx + 1, 1]),
                    QBrush(Qt.black),
                )

    def doLifeCycle(self) -> None:
        self.d.clearCanvas()
        self.ph.doIter()
        self.setFPS()
        self.setAlpha()
        self.setStepSize()
        self.lock.acquire()
        self.drawLevyTrace()
        self.lock.release()

    def reset(self) -> None:
        self.ph.clearLevyPositions()
        self.ui.ResetButton.setEnabled(False)
        QTimer.singleShot(500, lambda: self.ui.ResetButton.setEnabled(True))

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.timer.stop()
        self.d.painter.end()
        return super().closeEvent(a0)


def guiMain(args):
    app = QApplication(args)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    guiMain(sys.argv)
