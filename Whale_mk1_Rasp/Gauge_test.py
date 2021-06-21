from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import math
import sys

class GaugeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.polygonColor = [[.00, Qt.red],
                            [.2, Qt.yellow],
                            [.7, Qt.green],
                            [1., Qt.transparent]]
        self.polygonColor_op1 = [[.25, QColor(78, 114, 237, 93)],
                            [.5, QColor(82, 162, 247, 97)],
                            [.75, QColor(86, 190, 224, 88)],
                            [1., QColor(82, 247, 245, 97)]]

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_Data)
        self.timer.start()

        self.setWindowTitle('Gauge Monitor')
        self.setFixedSize(740, 460)
        self.show()

    def update_Data(self):
        self.value = self.value + 1
        if self.value > 255:
            self.value = 0
        self.update()
    def paintEvent(self, event):
        self.drawGauge(100, 100, self.value)
        self.drawValue(100, 100, self.value)
    def drawValue(self, x_center, y_center, value):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        text = str(int(value))
        font = QFont("Decorative", 15)
        font.setBold(True)
        if value < 255 * 1/4:
            pen = QPen(QColor(82, 247, 245, 97))
        elif value < 255 * 2/4:
            pen = QPen(QColor(86, 190, 224, 88))
        elif value < 255 * 3/4:
            pen = QPen(QColor(82, 162, 247, 97))
        else:
            pen = QPen(QColor(78, 114, 237, 93))
        fm = QFontMetrics(font)
        w = fm.width(text) + 1
        h = fm.height()
        my_painter.setPen(pen)
        my_painter.setFont(font)
        my_painter.drawText(x_center - int(w/2), y_center - int(h/2), int(w), int(h), Qt.AlignCenter, text)
        my_painter.end()
    def drawGauge(self, x_center, y_center, value):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        gaugePolygon = QPolygon()

        for theta in range(135, int(135 + (270/255) * value)):
            x_1 = x_center + math.cos(math.radians(theta)) * 30
            y_1 = y_center + math.sin(math.radians(theta)) * 30
            gaugePolygon.append(QPoint(x_1, y_1))
        for length in range(30, 40):
            x_2 = x_center + math.cos(math.radians(135 + (270/255) * value)) * length
            y_2 = y_center + math.sin(math.radians(135 + (270/255) * value)) * length
            gaugePolygon.append(QPoint(x_2, y_2))
        for theta in range(int(135 + (270/255) * value), 135, -1):
            x_1 = x_center + math.cos(math.radians(theta)) * 40
            y_1 = y_center + math.sin(math.radians(theta)) * 40
            gaugePolygon.append(QPoint(x_1, y_1))
        for length in range(40, 30, -1):
            x_2 = x_center + math.cos(math.radians(135)) * length
            y_2 = y_center + math.sin(math.radians(135)) * length
            gaugePolygon.append(QPoint(x_2, y_2))
        my_painter.setPen(QPen(Qt.NoPen))
        grad = QConicalGradient(QPointF(x_center, y_center), -45)
        for eachColor in self.polygonColor_op1:
            grad.setColorAt(eachColor[0], eachColor[1])
        my_painter.setBrush(grad)
        my_painter.drawPolygon(gaugePolygon)
        my_painter.end()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GaugeApp()
    sys.exit(app.exec_())