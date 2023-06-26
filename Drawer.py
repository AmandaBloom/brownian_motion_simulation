from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
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
        # Check for NaN
        if x == x and y == y and r == r:
            self.painter.drawEllipse(x, y, r, r)

    def drawLine(self, x1: int, y1: int, x2: int, y2: int, brush_col: QBrush) -> None:
        self.painter.setBrush(QBrush(brush_col))
        if x1 == x1 and y1 == y1 and x2 == x2 and y2 == y2:
            self.painter.drawLine(x1, y1, x2, y2)

    def stop(self):
        self.painter.end()
        self.canvas.fill(QColor(255, 102, 179))

    def clearCanvas(self) -> None:
        self.painter.end()
        self.canvas.fill(QColor(255, 102, 179))
        self.label.setPixmap(self.canvas)
        self.painter = QPainter(self.label.pixmap())

    def drawCircles(self, point_list: list[int, int, int]) -> None:
        for point in point_list:
            self.drawCircle(point.x, point.y, point.r)
