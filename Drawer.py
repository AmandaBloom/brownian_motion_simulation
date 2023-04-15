from PyQt5.QtGui import QPixmap, QPainter, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700


class Drawer:
    def __init__(self, label: QLabel) -> None:
        self.label = label

        self.canvas = QPixmap(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.canvas.fill(Qt.white)
        self.label.setPixmap(self.canvas)
        self.painter = QPainter(self.label.pixmap())

    def drawCircle(self, x: int, y: int, r: int, brush_col: QBrush) -> None:
        self.painter.setBrush(QBrush(brush_col))
        self.painter.drawEllipse(x, y, 2 * r, 2 * r)

    def clearCanvas(self) -> None:
        self.painter.end()
        self.canvas.fill(Qt.white)
        self.label.setPixmap(self.canvas)
        self.painter = QPainter(self.label.pixmap())

    def drawCircles(self, point_list: list[int, int, int]) -> None:
        for point in point_list:
            self.drawCircle(point.x, point.y, point.r)
