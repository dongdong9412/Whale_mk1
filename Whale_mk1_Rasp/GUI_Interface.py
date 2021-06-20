import sys
import cv2
import serial
import serial.tools.list_ports as sp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

def Update_USBPort(connected):
    list = sp.comports()

    for i in list:
        connected.append(i.device)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time = QTime.currentTime()
        self.initUI()
        

    def initUI(self):
        self.activeColor = QColor(232, 84, 108, 91)
        self.deactiveColor = QColor(255, 114, 92, 100)
        # Image Configure #
        self.rangeImage = QLabel()
        self.img = cv2.imread('images.png')
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = cv2.resize(self.img, dsize=(300,300), interpolation=cv2.INTER_AREA)
        self.h, self.w, self.c = self.img.shape
        self.image = QImage(self.img.data, self.w, self.h, self.w*self.c, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(self.image)
        self.rangeImage.setPixmap(self.pixmap)
        self.rangeImage.move(30,30)
        
        # Slider Configure #
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setGeometry(30, 340, 10, 100)
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(2)

        # Dial Configure #
        #self.dial = QDial(self)
        #self.dial.setGeometry(100, 340, 100, 100)
        #self.dial.setRange(0, 100)

        # Progress Bar Configure #
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 450, 200, 25)
        self.step = 0

        #self.slider.valueChanged.connect(self.dial.setValue)
        
        # Button Configure #
        self.bt_Start = QPushButton('Connect', self)
        self.bt_Start.setGeometry(125, 10, 90, 25)
        self.bt_Start.clicked.connect(self.doAction)

        self.bt_Quit = QPushButton('Quit', self)
        self.bt_Quit.setGeometry(600, 450, 90, 25)
        self.bt_Quit.resize(self.bt_Quit.sizeHint())
        self.bt_Quit.clicked.connect(QCoreApplication.instance().quit)

        # Combobox Configure #
        self.serialList = QComboBox(self)
        self.comList = []
        Update_USBPort(self.comList)
        self.serialList.addItems(self.comList)
        self.serialList.setGeometry(20, 10, 100, 25)

        # Status Bar Configure #
        self.statusBar().showMessage('Ready\t' + self.time.toString(Qt.DefaultLocaleLongDate))

        # Timer Configure #
        self.timer = QBasicTimer()

        self.setWindowTitle('Whale Mark 1')
        self.setWindowIcon(QIcon('images_1.png'))
        # self.setGeometry(300, 300, 300, 200)
        self.setFixedSize(700, 500)
        self.center()
        self.show()
    
    # Paint Event #
    def paintEvent(self, event):
        self.draw_Gauge(135,390, 100, 28, 40)

    def draw_Gauge(self, x_center, y_center, value, innerSize, outerSize):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        self.pen = QPen(QColor(197, 84, 232, 91))
        text = str(int(value))
        font = QFont("Decorative", 15)
        font.setBold(True)
        fm = QFontMetrics(font)
        w = fm.width(text) + 1
        h = fm.height()
        my_painter.setPen(self.pen)
        my_painter.setFont(font)
        my_painter.drawText(x_center - int(w/2), y_center - int(h/2), int(w), int(h), Qt.AlignCenter, text)

        if value > 0:
            self.pen = QPen(self.activeColor)
        else:
            self.pen = QPen(self.deactiveColor)
        self.pen.setWidth(3)
        my_painter.setPen(self.pen)

        
        for theta in range(90, 360+90, 8):
            if (theta - 90) > value * (360 / 255):
                self.pen = QPen(self.deactiveColor)
                my_painter.setPen(self.pen)
            x_1 = x_center + math.cos(math.radians(theta)) * innerSize
            y_1 = y_center + math.sin(math.radians(theta)) * innerSize
            x_2 = x_center + math.cos(math.radians(theta)) * outerSize
            y_2 = y_center + math.sin(math.radians(theta)) * outerSize
            my_painter.drawLine(int(x_1), int(y_1), int(x_2), int(y_2))

        my_painter.end()

    # Timer Event #
    def timerEvent(self, e):
        self.step = self.step + 1
        self.time = QTime.currentTime()
        self.statusBar().showMessage('Ready\t' + self.time.toString(Qt.DefaultLocaleLongDate))
        self.pbar.setValue(self.slider.value())

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.bt_Start.setText('Connect')
        else:
            self.timer.start(100, self)
            self.bt_Start.setText('Disconnect')
            
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())