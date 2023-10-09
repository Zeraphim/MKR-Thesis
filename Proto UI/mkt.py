from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(568, 536)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Picture_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.Picture_graphicsView.setGeometry(QtCore.QRect(30, 100, 311, 211))
        self.Picture_graphicsView.setObjectName("Picture_graphicsView")
        self.captureBtn = QtWidgets.QPushButton(self.centralwidget)
        self.captureBtn.setGeometry(QtCore.QRect(390, 80, 113, 32))
        self.captureBtn.setObjectName("captureBtn")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 571, 61))
        self.frame.setStyleSheet("background-color: blue;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 501, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")
        self.resetBtn = QtWidgets.QPushButton(self.centralwidget)
        self.resetBtn.setGeometry(QtCore.QRect(380, 280, 141, 51))
        self.resetBtn.setObjectName("resetBtn")
        self.translateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.translateBtn.setGeometry(QtCore.QRect(380, 160, 141, 51))
        self.translateBtn.setObjectName("translateBtn")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 350, 71, 16))
        self.label_3.setObjectName("label_3")
        self.translationTxt = QtWidgets.QTextBrowser(self.centralwidget)
        self.translationTxt.setGeometry(QtCore.QRect(100, 350, 441, 51))
        self.translationTxt.setObjectName("translationTxt")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 430, 71, 16))
        self.label_4.setObjectName("label_4")
        self.autoTranslateTxt = QtWidgets.QTextBrowser(self.centralwidget)
        self.autoTranslateTxt.setGeometry(QtCore.QRect(100, 430, 441, 51))
        self.autoTranslateTxt.setObjectName("autoTranslateTxt")
        self.autocorrectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.autocorrectBtn.setGeometry(QtCore.QRect(380, 220, 141, 51))
        self.autocorrectBtn.setObjectName("autocorrectBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Camera Capture
        self.timer = QtCore.QTimer()
        self.scene = QGraphicsScene()
        # Set the scene for the QGraphicsView
        self.Picture_graphicsView.setScene(self.scene)

        self.captureBtn.clicked.connect(self.capture_and_save)
        # Disable the capture button initially
        self.captureBtn.setEnabled(True)

        # Start capturing at the beginning
        self.start_camera()

        # Reset Btn
        self.resetBtn.clicked.connect(self.reset_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "OCR Handrwiting Detection"))
        self.captureBtn.setText(_translate("MainWindow", "CAPTURE"))
        self.label_2.setText(_translate(
            "MainWindow", "OCR Handwriting Detection"))
        self.resetBtn.setText(_translate("MainWindow", "RESET"))
        self.translateBtn.setText(_translate("MainWindow", "TRANSLATE"))
        self.label_3.setText(_translate("MainWindow", "Translation:"))
        self.label_4.setText(_translate("MainWindow", "Autocorrect"))
        self.autocorrectBtn.setText(_translate("MainWindow", "AUTOCORRECT"))

    def start_camera(self):
        # 0 for the default camera (you can change it if you have multiple cameras)
        self.cap = cv2.VideoCapture(0)

        # Reconnect the timer to the update_frame method
        self.timer.timeout.connect(self.update_frame)

        # Start the timer
        self.timer.start(30)  # Update the frame every 30 milliseconds

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Get the dimensions of the QGraphicsView
            view_width = self.Picture_graphicsView.width()
            view_height = self.Picture_graphicsView.height()

            # Resize the frame to fit the QGraphicsView dimensions
            frame = cv2.resize(frame, (view_width, view_height))

            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height,
                          bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.scene.clear()  # Clear the previous frame
            self.scene.addPixmap(pixmap)

    def capture_and_save(self):
        # Disable camera capture by stopping the timer
        self.timer.stop()

        ret, frame = self.cap.read()
        if ret:
            # Save the captured frame as '0.tif' in the script's directory
            cv2.imwrite('0.tif', frame)

        # Release the camera capture to disable it
        self.cap.release()

        image = QtGui.QPixmap("0.tif")
        scaled_image = image.scaled(self.Picture_graphicsView.size(),
                                    QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(scaled_image)

        self.Picture_graphicsView.setScene(scene)
        self.Picture_graphicsView.fitInView(
            scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.Picture_graphicsView.centerOn(scene.sceneRect().center())

    def reset_clicked(self):

        # Delete '0.tif' file if it exists
        if os.path.exists('0.tif'):
            os.remove('0.tif')

        # Camera Capture
        self.timer = QtCore.QTimer()
        self.scene = QGraphicsScene()
        # Set the scene for the QGraphicsView
        self.Picture_graphicsView.setScene(self.scene)

        self.start_camera()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
