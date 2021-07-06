from PyQt5 import QtGui
import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *




class MyApp(QWidget):
    capture = cv2.VideoCapture(0)
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.image_region = QLabel(self)
        self.image_region.move(5, 5)
        
        self.timer = QTimer(self)
        self.timer.setInterval(int(1/60*1000))
        self.timer.timeout.connect(self.updateFrame)

        self.timer.start()
        self.setWindowTitle('WebCam')
        self.resize(600, 340)
        self.show()

    def updateFrame(self):
        while True:
            ret, frame = self.capture.read()
            frame = cv2.resize(frame, dsize=(320,240), interpolation=cv2.INTER_AREA)
            color_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = frame.shape
            self.image_region.resize(w, h)
            qt_frame = QImage(color_image.data,
                            w,
                            h,
                            w*c,
                            QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qt_frame)
            self.image_region.setPixmap(pixmap)
            if cv2.waitKey(1) == ord('q'):
                self.capture.release()
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())