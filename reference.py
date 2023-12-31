# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WH-Detection.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os
import shutil
import time

file_path_global = ""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 663)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 120, 341, 211))
        self.graphicsView.setObjectName("graphicsView")
        self.browseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.browseBtn.setGeometry(QtCore.QRect(10, 70, 113, 32))
        self.browseBtn.setObjectName("browseBtn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 75, 411, 21))
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 571, 61))
        self.frame.setStyleSheet("background-color: red;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 501, 41))
        font = QtGui.QFont()
        font.setFamily("Futura")
        font.setPointSize(36)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white;")
        self.label_2.setObjectName("label_2")
        self.translateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.translateBtn.setGeometry(QtCore.QRect(390, 190, 141, 51))
        self.translateBtn.setObjectName("translateBtn")
        self.translateBtn.clicked.connect(self.detect_button_clicked)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 350, 71, 16))
        self.label_3.setObjectName("label_3")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(20, 380, 501, 241))
        self.graphicsView_2.setObjectName("graphicsView_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.file_path_global = ""
        self.file_name = ""

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the browse button to a function
        self.browseBtn.clicked.connect(self.browse_image)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Water Hyacinth Detection"))
        self.browseBtn.setText(_translate("MainWindow", "BROWSE"))
        self.label.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate(
            "MainWindow", "Water Hyacinth Detection"))
        self.translateBtn.setText(_translate("MainWindow", "DETECT"))
        self.label_3.setText(_translate("MainWindow", "Result:"))

    def browse_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        self.file_path_global = file_path
        filename = os.path.basename(file_path)
        self.filename = filename

        try:
            # Delete the "yolov7/runs" folder
            runs_folder = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "yolov7", "runs")
            shutil.rmtree(runs_folder)
        except:
            pass

        if file_path:
            global_file_path = file_path  # Assign the value to the global variable
            self.label.setText(file_path)
            self.show_image(file_path)

        if file_path:
            self.label.setText(file_path)
            self.show_image(file_path)

    def show_image(self, image_path):
        image = QtGui.QPixmap(image_path)
        scaled_image = image.scaled(self.graphicsView.size(
        ), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(scaled_image)

        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(
            scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.graphicsView.centerOn(scene.sceneRect().center())

    def detect_button_clicked(self):
        process = subprocess.Popen(['open', 'Detect'])
        process.wait()  # Wait for the process to finish

        time.sleep(10)

        # Once the process finishes, show the image in graphicsView_2
        current_directory = os.getcwd()
        current_directory = current_directory + "/yolov7/runs/detect/exp/"

        detection_image_dir = current_directory + '1.jpg'
        self.show_detection(detection_image_dir)

    def show_detection(self, image_path):

        image = QtGui.QPixmap(image_path)
        scaled_image = image.scaled(self.graphicsView.size(
        ), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(scaled_image)

        self.graphicsView_2.setScene(scene)
        self.graphicsView_2.fitInView(
            scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.graphicsView_2.centerOn(scene.sceneRect().center())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
