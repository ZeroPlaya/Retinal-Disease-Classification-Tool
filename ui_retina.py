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
        self.imagePlaceholder = QLabel(self.ClassificationPage)
        self.imagePlaceholder.setObjectName(u"imagePlaceholder")
        self.imagePlaceholder.setGeometry(QRect(8, 100, 383, 254))
        self.imagePlaceholder.setStyleSheet(u"")
        self.imagePlaceholder.setPixmap(QPixmap(u"C:/Users/kurtd/Desktop/New Dataset/Age-Related Macular Degeneration/25.png"))
        self.imagePlaceholder.setScaledContents(True)
        self.uploadNewImageButton = QPushButton(self.ClassificationPage)
        self.uploadNewImageButton.setObjectName(u"uploadNewImageButton")
        self.uploadNewImageButton.setGeometry(QRect(8, 370, 144, 57))
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
        self.saveResultsButton.setGeometry(QRect(161, 370, 127, 57))
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
        self.widget.setGeometry(QRect(390, 101, 310, 247))
        self.widget.setMinimumSize(QSize(310, 247))
        self.widget.setMaximumSize(QSize(310, 247))
        self.widget.setStyleSheet(u"QWidget {\n"
"    background-image: url(:images/assets/resultsbg.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"")
        self.resultPlaceholder1_2 = QLabel(self.widget)
        self.resultPlaceholder1_2.setObjectName(u"resultPlaceholder1_2")
        self.resultPlaceholder1_2.setGeometry(QRect(40, 79, 151, 41))
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
        self.resultPlaceholder1_2.setPalette(palette)
        font1 = QFont()
        font1.setBold(False)
        font1.setItalic(True)
        self.resultPlaceholder1_2.setFont(font1)
        self.resultPlaceholder1_2.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.resultPlaceholder1_2.setLineWidth(0)
        self.resultPlaceholder1_2.setWordWrap(True)
        self.resultPlaceholder2_2 = QLabel(self.widget)
        self.resultPlaceholder2_2.setObjectName(u"resultPlaceholder2_2")
        self.resultPlaceholder2_2.setGeometry(QRect(40, 120, 141, 41))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.resultPlaceholder2_2.setPalette(palette1)
        self.resultPlaceholder2_2.setFont(font1)
        self.resultPlaceholder2_2.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.resultPlaceholder2_2.setWordWrap(True)
        self.resultPlaceholder3_2 = QLabel(self.widget)
        self.resultPlaceholder3_2.setObjectName(u"resultPlaceholder3_2")
        self.resultPlaceholder3_2.setGeometry(QRect(40, 160, 141, 41))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Text, brush)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush1)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.resultPlaceholder3_2.setPalette(palette2)
        self.resultPlaceholder3_2.setFont(font1)
        self.resultPlaceholder3_2.setStyleSheet(u"QLabel {\n"
"    background-color: white; /* Solid white background */\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.resultPlaceholder3_2.setWordWrap(True)
        self.ClassificationResults_2 = QLabel(self.widget)
        self.ClassificationResults_2.setObjectName(u"ClassificationResults_2")
        self.ClassificationResults_2.setGeometry(QRect(40, 30, 231, 41))
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush3 = QBrush(QColor(0, 0, 0, 0))
        brush3.setStyle(Qt.SolidPattern)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush3)
        palette3.setBrush(QPalette.Active, QPalette.Text, brush)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush3)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush2)
#endif
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush3)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush2)
#endif
        self.ClassificationResults_2.setPalette(palette3)
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        self.ClassificationResults_2.setFont(font2)
        self.ClassificationResults_2.setStyleSheet(u"QLabel {\n"
"    background-color: transparent;\n"
"    color: black; /* Ensure text stays visible */\n"
"}\n"
"")
        self.ClassificationResults_2.setFrameShadow(QFrame.Plain)
        self.ClassificationResults_2.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(self.ClassificationPage)
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
        self.tableWidget = QTableWidget(self.widget_2)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget.rowCount() < 1):
            self.tableWidget.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setItem(0, 2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setItem(0, 3, __qtablewidgetitem8)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(20, 80, 631, 331))
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setStyleSheet(u"/* Table cells */\n"
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
        self.tableWidget.setFrameShadow(QFrame.Sunken)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
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
        self.tableWidget.raise_()

        self.verticalLayout.addWidget(self.widget_2)

        self.stackedWidget.addWidget(self.HistoryPage)

        self.gridLayout_4.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(RetinalDiseaseClassifier)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RetinalDiseaseClassifier)
    # setupUi

    def retranslateUi(self, RetinalDiseaseClassifier):
        RetinalDiseaseClassifier.setWindowTitle(QCoreApplication.translate("RetinalDiseaseClassifier", u"Retinal Disease Classification", None))
        self.Title.setText("")
        self.getStartedButton.setText("")
        self.uploadBackButton.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"<-", None))
        self.uploadImageButton.setText("")
        self.historyButton.setText("")
        self.imagePlaceholder.setText("")
        self.uploadNewImageButton.setText("")
        self.saveResultsButton.setText("")
        self.classificationBackButton.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"<-", None))
        self.resultPlaceholder1_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Diabetic Retinopathy (92.5%)", None))
        self.resultPlaceholder2_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Myopia (6.5%)", None))
        self.resultPlaceholder3_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Central Serous Retinopathy (1.0%)", None))
        self.ClassificationResults_2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Classification Results", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Image", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Patient Name", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Date", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"Results", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"001", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem5 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"IMG_0065", None));
        ___qtablewidgetitem6 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"John Doe", None));
        ___qtablewidgetitem7 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"02/21/25", None));
        ___qtablewidgetitem8 = self.tableWidget.item(0, 3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RetinalDiseaseClassifier", u"ARMD, CRVO, MY", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.historyBackButton.setText("")
    # retranslateUi

