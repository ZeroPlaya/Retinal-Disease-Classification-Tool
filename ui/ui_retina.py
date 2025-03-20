# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'retina.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import rc_resources

class Ui_RetinalDiseaseClassifier(object):
    def setupUi(self, RetinalDiseaseClassifier):
        if not RetinalDiseaseClassifier.objectName():
            RetinalDiseaseClassifier.setObjectName(u"RetinalDiseaseClassifier")
        RetinalDiseaseClassifier.resize(720, 512)
        RetinalDiseaseClassifier.setMinimumSize(QSize(720, 512))
        RetinalDiseaseClassifier.setMaximumSize(QSize(720, 512))
        RetinalDiseaseClassifier.setAutoFillBackground(False)
        RetinalDiseaseClassifier.setStyleSheet(u"background-image: url(:/images/assets/bg.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"")
        self.gridLayout_4 = QGridLayout(RetinalDiseaseClassifier)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.stackedWidget = QStackedWidget(RetinalDiseaseClassifier)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMaximumSize(QSize(720, 512))
        self.stackedWidget.setStyleSheet(u"")
        self.MenuPage = QWidget()
        self.MenuPage.setObjectName(u"MenuPage")
        self.gridLayout = QGridLayout(self.MenuPage)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Title = QLabel(self.MenuPage)
        self.Title.setObjectName(u"Title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title.sizePolicy().hasHeightForWidth())
        self.Title.setSizePolicy(sizePolicy)
        self.Title.setMinimumSize(QSize(386, 330))
        self.Title.setMaximumSize(QSize(386, 330))
        font = QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QFont.PreferDefault)
        self.Title.setFont(font)
        self.Title.setStyleSheet(u"")
        self.Title.setFrameShape(QFrame.NoFrame)
        self.Title.setFrameShadow(QFrame.Plain)
        self.Title.setLineWidth(1)
        self.Title.setTextFormat(Qt.AutoText)
        self.Title.setPixmap(QPixmap(u":/images/assets/title.png"))
        self.Title.setScaledContents(True)
        self.Title.setAlignment(Qt.AlignCenter)
        self.Title.setWordWrap(True)

        self.gridLayout.addWidget(self.Title, 1, 1, 1, 1)

        self.getStartedButton = QPushButton(self.MenuPage)
        self.getStartedButton.setObjectName(u"getStartedButton")
        sizePolicy.setHeightForWidth(self.getStartedButton.sizePolicy().hasHeightForWidth())
        self.getStartedButton.setSizePolicy(sizePolicy)
        self.getStartedButton.setMinimumSize(QSize(387, 121))
        self.getStartedButton.setMaximumSize(QSize(387, 121))
        self.getStartedButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.getStartedButton.setAutoFillBackground(False)
        self.getStartedButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/getstarted.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")

        self.gridLayout.addWidget(self.getStartedButton, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.MenuPage)
        self.UploadPage = QWidget()
        self.UploadPage.setObjectName(u"UploadPage")
        self.UploadPage.setMinimumSize(QSize(720, 512))
        self.UploadPage.setMaximumSize(QSize(720, 512))
        self.uploadBackButton = QPushButton(self.UploadPage)
        self.uploadBackButton.setObjectName(u"uploadBackButton")
        self.uploadBackButton.setGeometry(QRect(8, 8, 66, 66))
        sizePolicy.setHeightForWidth(self.uploadBackButton.sizePolicy().hasHeightForWidth())
        self.uploadBackButton.setSizePolicy(sizePolicy)
        self.uploadBackButton.setMinimumSize(QSize(66, 66))
        self.uploadBackButton.setMaximumSize(QSize(66, 66))
        self.uploadBackButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.uploadBackButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/back.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.uploadImageButton = QPushButton(self.UploadPage)
        self.uploadImageButton.setObjectName(u"uploadImageButton")
        self.uploadImageButton.setGeometry(QRect(120, 90, 443, 176))
        self.uploadImageButton.setMinimumSize(QSize(443, 176))
        self.uploadImageButton.setMaximumSize(QSize(443, 176))
        self.uploadImageButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.uploadImageButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/upload.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.historyButton = QPushButton(self.UploadPage)
        self.historyButton.setObjectName(u"historyButton")
        self.historyButton.setGeometry(QRect(120, 260, 444, 177))
        self.historyButton.setMinimumSize(QSize(444, 177))
        self.historyButton.setMaximumSize(QSize(444, 177))
        self.historyButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.historyButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/history.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.stackedWidget.addWidget(self.UploadPage)
        self.ClassificationPage = QWidget()
        self.ClassificationPage.setObjectName(u"ClassificationPage")
        self.uploadNewImageButton = QPushButton(self.ClassificationPage)
        self.uploadNewImageButton.setObjectName(u"uploadNewImageButton")
        self.uploadNewImageButton.setGeometry(QRect(8, 391, 144, 57))
        self.uploadNewImageButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.uploadNewImageButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/uploadnew.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.saveResultsButton = QPushButton(self.ClassificationPage)
        self.saveResultsButton.setObjectName(u"saveResultsButton")
        self.saveResultsButton.setGeometry(QRect(161, 391, 127, 57))
        self.saveResultsButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveResultsButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/save.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.classificationBackButton = QPushButton(self.ClassificationPage)
        self.classificationBackButton.setObjectName(u"classificationBackButton")
        self.classificationBackButton.setGeometry(QRect(8, 8, 66, 66))
        sizePolicy.setHeightForWidth(self.classificationBackButton.sizePolicy().hasHeightForWidth())
        self.classificationBackButton.setSizePolicy(sizePolicy)
        self.classificationBackButton.setMinimumSize(QSize(66, 66))
        self.classificationBackButton.setMaximumSize(QSize(66, 66))
        self.classificationBackButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.classificationBackButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/back.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.widget = QWidget(self.ClassificationPage)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(400, 50, 311, 367))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.widget.setMinimumSize(QSize(311, 367))
        self.widget.setMaximumSize(QSize(0, 0))
        self.widget.setStyleSheet(u"QWidget {\n"
"    background-image: url(:images/assets/classification results.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.resultPlaceholder = QLabel(self.widget)
        self.resultPlaceholder.setObjectName(u"resultPlaceholder")
        self.resultPlaceholder.setGeometry(QRect(37, 98, 231, 131))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(0, 0, 0, 128))
        brush2.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.resultPlaceholder.setPalette(palette)
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setItalic(True)
        self.resultPlaceholder.setFont(font1)
        self.resultPlaceholder.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.resultPlaceholder.setLineWidth(0)
        self.resultPlaceholder.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.resultPlaceholder.setWordWrap(True)
        self.nameLabel = QLabel(self.widget)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setGeometry(QRect(37, 36, 131, 16))
        font2 = QFont()
        font2.setFamilies([u"Inter"])
        font2.setPointSize(11)
        font2.setBold(True)
        self.nameLabel.setFont(font2)
        self.nameLabel.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateLabel = QLabel(self.widget)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setGeometry(QRect(161, 36, 111, 16))
        self.dateLabel.setFont(font2)
        self.dateLabel.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.nameValue = QLabel(self.widget)
        self.nameValue.setObjectName(u"nameValue")
        self.nameValue.setGeometry(QRect(37, 50, 131, 20))
        font3 = QFont()
        font3.setFamilies([u"Inter"])
        font3.setPointSize(8)
        font3.setBold(False)
        font3.setKerning(False)
        self.nameValue.setFont(font3)
        self.nameValue.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateValue = QLabel(self.widget)
        self.dateValue.setObjectName(u"dateValue")
        self.dateValue.setGeometry(QRect(161, 50, 111, 21))
        self.dateValue.setFont(font3)
        self.dateValue.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateValue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.remarkLabel = QLabel(self.widget)
        self.remarkLabel.setObjectName(u"remarkLabel")
        self.remarkLabel.setGeometry(QRect(50, 250, 91, 31))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush3 = QBrush(QColor(244, 244, 244, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.remarkLabel.setPalette(palette1)
        self.remarkLabel.setFont(font1)
        self.remarkLabel.setStyleSheet(u"QLabel {\n"
"    background-color: rgb(244, 244, 244); /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.remarkLabel.setWordWrap(True)
        self.remarkLabel_2 = QLabel(self.widget)
        self.remarkLabel_2.setObjectName(u"remarkLabel_2")
        self.remarkLabel_2.setGeometry(QRect(50, 274, 211, 41))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush3)
        palette2.setBrush(QPalette.Active, QPalette.Text, brush)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush3)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.remarkLabel_2.setPalette(palette2)
        font4 = QFont()
        font4.setFamilies([u"Inter"])
        font4.setPointSize(9)
        font4.setBold(False)
        font4.setItalic(False)
        self.remarkLabel_2.setFont(font4)
        self.remarkLabel_2.setStyleSheet(u"QLabel {\n"
"    background-color: rgb(244, 244, 244); /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.remarkLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.remarkLabel_2.setWordWrap(True)
        self.remarkLabel_2.setIndent(1)
        self.blackbg = QFrame(self.ClassificationPage)
        self.blackbg.setObjectName(u"blackbg")
        self.blackbg.setGeometry(QRect(10, 84, 390, 292))
        self.blackbg.setStyleSheet(u"QFrame {\n"
"    background-image: url(:images/assets/blackbg.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.imagePlaceholder = QLabel(self.blackbg)
        self.imagePlaceholder.setObjectName(u"imagePlaceholder")
        self.imagePlaceholder.setGeometry(QRect(170, 0, 50, 50))
        self.imagePlaceholder.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.imagePlaceholder.setAutoFillBackground(False)
        self.imagePlaceholder.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"}\n"
"")
        self.imagePlaceholder.setPixmap(QPixmap(u"C:/Users/kurtd/Desktop/New Dataset/Age-Related Macular Degeneration/25.png"))
        self.imagePlaceholder.setScaledContents(True)
        self.imageName = QLabel(self.blackbg)
        self.imageName.setObjectName(u"imageName")
        self.imageName.setGeometry(QRect(169, 266, 211, 20))
        self.imageName.setLayoutDirection(Qt.LeftToRight)
        self.imageName.setStyleSheet(u"QLabel {\n"
"background-color: transparent; \n"
"color: white;\n"
"}")
        self.imageName.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.stackedWidget.addWidget(self.ClassificationPage)
        self.blackbg.raise_()
        self.uploadNewImageButton.raise_()
        self.saveResultsButton.raise_()
        self.classificationBackButton.raise_()
        self.widget.raise_()
        self.historyViewer = QWidget()
        self.historyViewer.setObjectName(u"historyViewer")
        self.historyViewBackButton = QPushButton(self.historyViewer)
        self.historyViewBackButton.setObjectName(u"historyViewBackButton")
        self.historyViewBackButton.setGeometry(QRect(8, 8, 66, 66))
        sizePolicy.setHeightForWidth(self.historyViewBackButton.sizePolicy().hasHeightForWidth())
        self.historyViewBackButton.setSizePolicy(sizePolicy)
        self.historyViewBackButton.setMinimumSize(QSize(66, 66))
        self.historyViewBackButton.setMaximumSize(QSize(66, 66))
        self.historyViewBackButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.historyViewBackButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/back.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.modifyButton = QPushButton(self.historyViewer)
        self.modifyButton.setObjectName(u"modifyButton")
        self.modifyButton.setGeometry(QRect(8, 391, 144, 57))
        self.modifyButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.modifyButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/modifyrecord.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.saveChangesButton = QPushButton(self.historyViewer)
        self.saveChangesButton.setObjectName(u"saveChangesButton")
        self.saveChangesButton.setGeometry(QRect(161, 391, 127, 57))
        self.saveChangesButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveChangesButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/save.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.blackbg_2 = QFrame(self.historyViewer)
        self.blackbg_2.setObjectName(u"blackbg_2")
        self.blackbg_2.setGeometry(QRect(10, 84, 390, 292))
        self.blackbg_2.setStyleSheet(u"QFrame {\n"
"    background-image: url(:images/assets/blackbg.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.imagePlaceholder_2 = QLabel(self.blackbg_2)
        self.imagePlaceholder_2.setObjectName(u"imagePlaceholder_2")
        self.imagePlaceholder_2.setGeometry(QRect(170, 0, 50, 50))
        self.imagePlaceholder_2.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.imagePlaceholder_2.setAutoFillBackground(False)
        self.imagePlaceholder_2.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"}\n"
"")
        self.imagePlaceholder_2.setPixmap(QPixmap(u"C:/Users/kurtd/Desktop/New Dataset/Age-Related Macular Degeneration/25.png"))
        self.imagePlaceholder_2.setScaledContents(True)
        self.imageName_2 = QLabel(self.blackbg_2)
        self.imageName_2.setObjectName(u"imageName_2")
        self.imageName_2.setGeometry(QRect(169, 266, 211, 20))
        self.imageName_2.setLayoutDirection(Qt.LeftToRight)
        self.imageName_2.setStyleSheet(u"QLabel {\n"
"background-color: transparent; \n"
"color: white;\n"
"}")
        self.imageName_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ResultInfo = QWidget(self.historyViewer)
        self.ResultInfo.setObjectName(u"ResultInfo")
        self.ResultInfo.setGeometry(QRect(400, 50, 311, 367))
        sizePolicy1.setHeightForWidth(self.ResultInfo.sizePolicy().hasHeightForWidth())
        self.ResultInfo.setSizePolicy(sizePolicy1)
        self.ResultInfo.setMinimumSize(QSize(311, 367))
        self.ResultInfo.setMaximumSize(QSize(0, 0))
        self.ResultInfo.setStyleSheet(u"QWidget {\n"
"    background-image: url(:images/assets/classification results.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.resultPlaceholder_2 = QLabel(self.ResultInfo)
        self.resultPlaceholder_2.setObjectName(u"resultPlaceholder_2")
        self.resultPlaceholder_2.setGeometry(QRect(37, 98, 231, 131))
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Text, brush)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.resultPlaceholder_2.setPalette(palette3)
        self.resultPlaceholder_2.setFont(font1)
        self.resultPlaceholder_2.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.resultPlaceholder_2.setLineWidth(0)
        self.resultPlaceholder_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.resultPlaceholder_2.setWordWrap(True)
        self.nameLabel_2 = QLabel(self.ResultInfo)
        self.nameLabel_2.setObjectName(u"nameLabel_2")
        self.nameLabel_2.setGeometry(QRect(37, 36, 131, 16))
        self.nameLabel_2.setFont(font2)
        self.nameLabel_2.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateLabel_2 = QLabel(self.ResultInfo)
        self.dateLabel_2.setObjectName(u"dateLabel_2")
        self.dateLabel_2.setGeometry(QRect(161, 36, 111, 16))
        self.dateLabel_2.setFont(font2)
        self.dateLabel_2.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateLabel_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.nameValue_2 = QLabel(self.ResultInfo)
        self.nameValue_2.setObjectName(u"nameValue_2")
        self.nameValue_2.setGeometry(QRect(37, 50, 131, 20))
        self.nameValue_2.setFont(font3)
        self.nameValue_2.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateValue_2 = QLabel(self.ResultInfo)
        self.dateValue_2.setObjectName(u"dateValue_2")
        self.dateValue_2.setGeometry(QRect(161, 50, 111, 21))
        self.dateValue_2.setFont(font3)
        self.dateValue_2.setStyleSheet(u"QLabel {\n"
"    background-color: transparent; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.dateValue_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.remarkLabel_13 = QLabel(self.ResultInfo)
        self.remarkLabel_13.setObjectName(u"remarkLabel_13")
        self.remarkLabel_13.setGeometry(QRect(50, 250, 91, 31))
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Button, brush3)
        palette4.setBrush(QPalette.Active, QPalette.Text, brush)
        palette4.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush3)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette4.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Button, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.Button, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.remarkLabel_13.setPalette(palette4)
        self.remarkLabel_13.setFont(font1)
        self.remarkLabel_13.setStyleSheet(u"QLabel {\n"
"    background-color: rgb(244, 244, 244); /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.remarkLabel_13.setWordWrap(True)
        self.remarkValue_2 = QLabel(self.ResultInfo)
        self.remarkValue_2.setObjectName(u"remarkValue_2")
        self.remarkValue_2.setGeometry(QRect(50, 274, 211, 41))
        palette5 = QPalette()
        palette5.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Active, QPalette.Button, brush3)
        palette5.setBrush(QPalette.Active, QPalette.Text, brush)
        palette5.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Active, QPalette.Base, brush3)
        palette5.setBrush(QPalette.Active, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette5.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Button, brush3)
        palette5.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette5.setBrush(QPalette.Inactive, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette5.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Button, brush3)
        palette5.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        palette5.setBrush(QPalette.Disabled, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.remarkValue_2.setPalette(palette5)
        self.remarkValue_2.setFont(font4)
        self.remarkValue_2.setStyleSheet(u"QLabel {\n"
"    background-color: rgb(244, 244, 244); /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.remarkValue_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.remarkValue_2.setWordWrap(True)
        self.remarkValue_2.setIndent(1)
        self.nameLabel_3 = QLabel(self.historyViewer)
        self.nameLabel_3.setObjectName(u"nameLabel_3")
        self.nameLabel_3.setGeometry(QRect(210, 20, 131, 16))
        self.nameLabel_3.setFont(font2)
        self.nameLabel_3.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.stackedWidget.addWidget(self.historyViewer)
        self.HistoryPage = QWidget()
        self.HistoryPage.setObjectName(u"HistoryPage")
        self.verticalLayout = QVBoxLayout(self.HistoryPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(self.HistoryPage)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setStyleSheet(u"QWidget {\n"
"    background-image: url(:images/assets/historybg.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.historyTable = QTableWidget(self.widget_2)
        if (self.historyTable.columnCount() < 6):
            self.historyTable.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.historyTable.rowCount() < 1):
            self.historyTable.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.historyTable.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.historyTable.setItem(0, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.historyTable.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.historyTable.setItem(0, 2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.historyTable.setItem(0, 3, __qtablewidgetitem8)
        self.historyTable.setObjectName(u"historyTable")
        self.historyTable.setGeometry(QRect(20, 80, 631, 331))
        self.historyTable.setAutoFillBackground(False)
        self.historyTable.setStyleSheet(u"/* Table cells */\n"
"QTableWidget {\n"
"    background: white;\n"
"    color: black;\n"
"    gridline-color: lightgray; /* Light gray gridlines */\n"
"    border: none; /* Removes outer border */\n"
"}\n"
"\n"
"/* Column headers */\n"
"QHeaderView::section {\n"
"    background: white;\n"
"    color: black;\n"
"    border: none; /* Removes header border */\n"
"}\n"
"\n"
"/* Left row headers */\n"
"QTableCornerButton::section, QHeaderView::section:vertical {\n"
"    background: #f0f0f0; /* Light gray */\n"
"    color: black;\n"
"    border: none; /* Removes row header border */\n"
"}\n"
"")
        self.historyTable.setFrameShadow(QFrame.Sunken)
        self.historyTable.setLineWidth(0)
        self.historyTable.setShowGrid(True)
        self.historyTable.setGridStyle(Qt.SolidLine)
        self.historyTable.setColumnCount(6)
        self.historyTable.horizontalHeader().setVisible(True)
        self.historyTable.verticalHeader().setVisible(False)
        self.historyBackButton = QPushButton(self.widget_2)
        self.historyBackButton.setObjectName(u"historyBackButton")
        self.historyBackButton.setGeometry(QRect(8, 8, 66, 66))
        sizePolicy.setHeightForWidth(self.historyBackButton.sizePolicy().hasHeightForWidth())
        self.historyBackButton.setSizePolicy(sizePolicy)
        self.historyBackButton.setMinimumSize(QSize(66, 66))
        self.historyBackButton.setMaximumSize(QSize(66, 66))
        self.historyBackButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.historyBackButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-image: url(:images/assets/invisback.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.line = QFrame(self.widget_2)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(12, 60, 656, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.historyBackButton.raise_()
        self.line.raise_()
        self.historyTable.raise_()

        self.verticalLayout.addWidget(self.widget_2)

        self.stackedWidget.addWidget(self.HistoryPage)

        self.gridLayout_4.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(RetinalDiseaseClassifier)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(RetinalDiseaseClassifier)
    # setupUi

    def retranslateUi(self, RetinalDiseaseClassifier):
        RetinalDiseaseClassifier.setWindowTitle(QCoreApplication.translate("RetinalDiseaseClassifier", u"Retinal Disease Classification", None))
        self.Title.setText("")
        self.getStartedButton.setText("")
        self.uploadBackButton.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"<-", None))
        self.uploadImageButton.setText("")
        self.historyButton.setText("")
        self.uploadNewImageButton.setText("")
        self.saveResultsButton.setText("")
        self.classificationBackButton.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"<-", None))
        self.resultPlaceholder.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Diabetic Retinopathy (92.5%)", None))
        self.nameLabel.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Patient's Name", None))
        self.dateLabel.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Date", None))
        self.nameValue.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Enter Name", None))
        self.dateValue.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"March 18, 2025", None))
        self.remarkLabel.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Remarks:", None))
        self.remarkLabel_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"abcd", None))
        self.imagePlaceholder.setText("")
        self.imageName.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"placeholder.png", None))
        self.historyViewBackButton.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"<-", None))
        self.modifyButton.setText("")
        self.saveChangesButton.setText("")
        self.imagePlaceholder_2.setText("")
        self.imageName_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"placeholder.png", None))
        self.resultPlaceholder_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Diabetic Retinopathy (92.5%)", None))
        self.nameLabel_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Patient's Name", None))
        self.dateLabel_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Date", None))
        self.nameValue_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Enter Name", None))
        self.dateValue_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"March 18, 2025", None))
        self.remarkLabel_13.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Remarks:", None))
        self.remarkValue_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"abcd", None))
        self.nameLabel_3.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"HISTORY VIEW", None))
        ___qtablewidgetitem = self.historyTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Image", None));
        ___qtablewidgetitem1 = self.historyTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Patient Name", None));
        ___qtablewidgetitem2 = self.historyTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Date", None));
        ___qtablewidgetitem3 = self.historyTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Results", None));
        ___qtablewidgetitem4 = self.historyTable.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"001", None));

        __sortingEnabled = self.historyTable.isSortingEnabled()
        self.historyTable.setSortingEnabled(False)
        ___qtablewidgetitem5 = self.historyTable.item(0, 0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"IMG_0065", None));
        ___qtablewidgetitem6 = self.historyTable.item(0, 1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"John Doe", None));
        ___qtablewidgetitem7 = self.historyTable.item(0, 2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"02/21/25", None));
        ___qtablewidgetitem8 = self.historyTable.item(0, 3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"ARMD, CRVO, MY", None));
        self.historyTable.setSortingEnabled(__sortingEnabled)

        self.historyBackButton.setText("")
    # retranslateUi

