import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget, QProgressBar, QSlider, QDial
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, QTime, Qt, QBasicTimer

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time = QTime.currentTime()
        self.initUI()

    def initUI(self):
        # Slider Configure #
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.move(30, 200)
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(2)

        # Dial Configure #
        self.dial = QDial(self)
        self.dial.move(100, 200)
        self.dial.setRange(0, 50)

        # Progress Bar Configure #
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.step = 0

        self.slider.valueChanged.connect(self.dial.setValue)
        
        # Button Configure #
        self.bt_Start = QPushButton('Start', self)
        self.bt_Start.move(40, 80)
        self.bt_Start.clicked.connect(self.doAction)

        self.bt_Quit = QPushButton('Quit', self)
        self.bt_Quit.move(50, 50)
        self.bt_Quit.resize(self.bt_Quit.sizeHint())
        self.bt_Quit.clicked.connect(QCoreApplication.instance().quit)

        # Status Bar Configure #
        self.statusBar().showMessage('Ready\t' + self.time.toString(Qt.DefaultLocaleLongDate))

        # Timer Configure #
        self.timer = QBasicTimer()

        self.setWindowTitle('Whale Mark 1')
        self.setWindowIcon(QIcon('images_1.png'))
        # self.setGeometry(300, 300, 300, 200)
        self.resize(500, 350)
        self.center()
        self.show()
    
    # Timer Event #
    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.bt_Start.setText('Finished')
            return
        self.step = self.step + 1
        self.time = QTime.currentTime()
        self.statusBar().showMessage('Ready\t' + self.time.toString(Qt.DefaultLocaleLongDate))
        self.pbar.setValue(self.slider.value())

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.bt_Start.setText('Start')
        else:
            self.timer.start(100, self)
            self.bt_Start.setText('Stop')
            
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())