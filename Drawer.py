from PyQt5.QtGui import QPixmap, QPainter, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

class Drawer:
    def __init__(self, label: QLabel) -> None:
        self.label = label
        
        self.canvas = QPixmap(700,700)
        self.canvas.fill(Qt.white)
        self.label.setPixmap(self.canvas)
        self.painter = QPainter(self.label.pixmap())

    def drawCircle(self, x, y, r) -> None:
        self.painter.setBrush(QBrush(Qt.red))
        self.painter.drawEllipse(x, y, 2*r, 2*r)

    def clearCanvas(self):
        self.painter.end()
        self.canvas.fill(Qt.white)
        self.label.setPixmap(self.canvas)
        self.painter = QPainter(self.label.pixmap())

    def drawCircles(self, point_list) -> None:
        for point in point_list:
            self.drawCircle(point.x, point.y, point.r)
