import cv2
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QScrollBar, QLabel, QTextBrowser, QTextEdit, \
    QLineEdit, QRadioButton, QSlider, QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import cv2 as cv
from detection_try import main
import atexit
import errno, os, stat, shutil

import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
import os


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("covidDetection.ui", self)
        self.convertButton = self.findChild(QPushButton, "convert")

        self.mainImage = self.findChild(QLabel, "mainImage")
        self.processedImage = self.findChild(QLabel, "newImage")
        self.fileButton = self.findChild(QPushButton, "openButton")
        self.path = self.findChild(QLabel, "label")
        self.slider = self.findChild(QSlider, "fileSlider")
        self.fileButton.clicked.connect(self.fileClicker)
        self.progressBar = self.findChild(QProgressBar, "progressBar")
        self.metricsLabel = self.findChild(QLabel, "metrics")

        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.sliderfunc)
        self.metrics = []

        self.show()

    def fileClicker(self):

        os.makedirs("test", exist_ok=True)
        os.makedirs("test/results_mask", exist_ok=True)
        os.makedirs("test/results", exist_ok=True)
        os.makedirs("test/original", exist_ok=True)
        self.fname = QFileDialog.getExistingDirectory(self, 'Open file')
        maskFile = QFileDialog.getExistingDirectory(self, 'Open file')
        covFile = QFileDialog.getExistingDirectory(self, 'Open file')
        print(self.fname)
        org_file = os.listdir(self.fname)
        print(org_file[0])

        for i in range(len(org_file)):
            try:

                org_photo = org_file[i][:-4]
                cov_mask = cv2.imread(f'{covFile}/{org_photo}.png', cv2.IMREAD_GRAYSCALE)
                lung_mask = cv2.imread(f'{maskFile}/{org_photo}.png', cv2.IMREAD_GRAYSCALE)
                image = cv.imread(f'{self.fname}/{org_photo}.jpg', cv2.IMREAD_GRAYSCALE)
                cv2.imwrite(f"test/original/{org_photo}.png", image)
                result = main(image, lung_mask, cov_mask)
                cv2.imwrite(f"test/results/{org_photo}.png", result[0])
                cv2.imwrite(f"test/results_mask/{org_photo}.png", result[1])
                self.metrics.append([result[1], result[2], result[3]])

                self.progressBar.setValue((i / len(org_file)) * 100)
            except:
                self.progressBar.setValue((i / len(org_file)) * 100)
                pass
        self.progressBar.setValue(100)
        print(self.metrics)

    def sliderfunc(self):
        self.lung_file = os.listdir("test/results")
        self.org_file = os.listdir("test/original")
        self.slider.setMaximum(len(self.lung_file) - 1)

        org_photo = self.org_file[self.slider.value()][:-4]
        lung_photo = self.lung_file[self.slider.value()][:-4]


        self.metricsLabel.setText(f'Accuracy: {self.metrics[self.slider.value()][0]} \n Precision: {self.metrics[self.slider.value()][1]} \n Recall: {self.metrics[self.slider.value()][2]}')
        self.mainImage.setPixmap(QPixmap(f"test/original/{org_photo}.png"))
        self.mainImage.setScaledContents(True)
        self.mainImage.setAlignment(QtCore.Qt.AlignCenter)
        self.processedImage.setPixmap(QPixmap(f"test/results/{lung_photo}.png"))
        self.processedImage.setScaledContents(True)
        self.processedImage.setAlignment(QtCore.Qt.AlignCenter)


if __name__ == "__main__":
    def handleRemoveReadonly(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(path)
        else:
            raise


    import sys

    app = QApplication(sys.argv)
    UIWindow = Ui()
    atexit.register(shutil.rmtree, 'test', ignore_errors=False, onerror=handleRemoveReadonly)
    app.exec_()
