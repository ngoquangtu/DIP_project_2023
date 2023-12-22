# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt,QDir)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget,QFileDialog)
from panorama import Panaroma
import imutils
import cv2

class Ui_MainWindow(object):
    def __init__(self):
        self.image_file_paths = []
        self.images = []
        self.x=1
        self.y=1
        self.dynamic_buttons = []
        self.max_in_row=5
        self.replace=None
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(887, 702)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 20, 71, 71))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(20, 330, 101, 31))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 300, 211, 151))
        self.label.setStyleSheet(u"background-color: rgb(197, 190, 190);")
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 370, 101, 31))
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(20, 410, 101, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 887, 17))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        
        self.pushButton_2.clicked.connect(lambda:self.uploadImage(MainWindow))
        self.pushButton_3.clicked.connect(lambda: self.upload_generate_image(MainWindow,self.generate_panorama_image(MainWindow)))
        self.pushButton_4.clicked.connect(self.clearAllImage)
        self.pushButton_5.clicked.connect(self.saveImage)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    def uploadImage(self,MainWindow):
        if self.x >= 10:
            self.y +=1
            self.x = 0
        file_path, _ = QFileDialog.getOpenFileName(MainWindow, "Open Image File", QDir.homePath())
        if file_path:
            self.replace = QLabel(self.centralwidget)
            self.replace.setScaledContents(True)
            self.replace.setGeometry(QRect( 20+self.x * 80, -60+self.y * 80, 71, 71))
            # self.replace.setText(QCoreApplication.translate("MainWindow", u"+", None))
            self.x += 1
            self.replace.setObjectName("pushButton1")
            pixmap = QPixmap(file_path) 
            self.replace.setPixmap(pixmap)
            self.replace.setStyleSheet(f"background-image: url({file_path}); background-repeat: no-repeat; background-position: center;")
            print(f"Button clicked! File path: {file_path}")
            self.replace.repaint()
            self.image_file_paths.append(file_path)
            self.dynamic_buttons.append(self.replace)
            self.replace.show()
    def generate_panorama_image(self,MainWindow):
        number_of_images=len(self.image_file_paths)
        images=[]
        for file_path in self.image_file_paths:
            image = cv2.imread(file_path)
            image = imutils.resize(image, width=400)
            image = imutils.resize(image, height=400)
            images.append(image)
        panaroma=Panaroma()
        if number_of_images < 2:
            self.statusbar.showMessage("Please upload at least two images for panorama generation.")
            return None  
        if number_of_images==2:
            (result, matched_points) = panaroma.image_stitch([images[0], images[1]], match_status=True)
        else:
            (result,matched_points)= panaroma.image_stitch([images[number_of_images-2],images[number_of_images-1]], match_status=True)
            for i in range(number_of_images-2):
                (result, matched_points) = panaroma.image_stitch([images[number_of_images-i-3],result], match_status=True)
        return result 
    
    def upload_generate_image(self,MainWindow,image):
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))
        self.label.repaint()
    def clearAllImage(self):
        self.images.clear()
        self.image_file_paths.clear()
        for label2 in self.dynamic_buttons:
            label2.hide()
            label2.clear()
        self.label.clear()
    def saveImage(self):
        if not self.label.pixmap():
            self.statusbar.showMessage("No image to save.")
            return
        file_path, _ = QFileDialog.getSaveFileName(None, "Save Image", QDir.homePath(), "Images (*.png *.jpg *.bmp);;All Files (*)")

        if file_path:
            # Get the current displayed pixmap from the label
            pixmap = self.label.pixmap()
            
            # Save the pixmap to the specified file path
            pixmap.save(file_path)

            self.statusbar.showMessage(f"Image saved to {file_path}")
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Generate Image", None))
        self.label.setText("")
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Clear Image", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Save Image", None))
    # retranslateUi

