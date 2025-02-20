# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'retinal_disease_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_RetinalDiseaseClassifier(object):
    def setupUi(self, RetinalDiseaseClassifier):
        if not RetinalDiseaseClassifier.objectName():
            RetinalDiseaseClassifier.setObjectName(u"RetinalDiseaseClassifier")
        RetinalDiseaseClassifier.resize(600, 400)
        self.verticalLayout = QVBoxLayout(RetinalDiseaseClassifier)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.imageLabel = QLabel(RetinalDiseaseClassifier)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFrameShape(QFrame.Box)

        self.verticalLayout.addWidget(self.imageLabel)

        self.uploadButton = QPushButton(RetinalDiseaseClassifier)
        self.uploadButton.setObjectName(u"uploadButton")

        self.verticalLayout.addWidget(self.uploadButton)

        self.classifyButton = QPushButton(RetinalDiseaseClassifier)
        self.classifyButton.setObjectName(u"classifyButton")

        self.verticalLayout.addWidget(self.classifyButton)

        self.resultLabel = QLabel(RetinalDiseaseClassifier)
        self.resultLabel.setObjectName(u"resultLabel")

        self.verticalLayout.addWidget(self.resultLabel)


        self.retranslateUi(RetinalDiseaseClassifier)

        QMetaObject.connectSlotsByName(RetinalDiseaseClassifier)
    # setupUi

    def retranslateUi(self, RetinalDiseaseClassifier):
        RetinalDiseaseClassifier.setWindowTitle(QCoreApplication.translate("RetinalDiseaseClassifier", u"Retinal Disease Classification", None))
        self.imageLabel.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"No Image Selected", None))
        self.uploadButton.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Upload Image", None))
        self.classifyButton.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Classify", None))
        self.resultLabel.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Result: ", None))
    # retranslateUi

