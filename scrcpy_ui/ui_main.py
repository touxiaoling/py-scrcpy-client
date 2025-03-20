# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(435, 616)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.combo_device = QComboBox(self.centralwidget)
        self.combo_device.setObjectName(u"combo_device")
        self.combo_device.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_4.addWidget(self.combo_device)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.combo_resolution = QComboBox(self.centralwidget)
        self.combo_resolution.addItem("")
        self.combo_resolution.addItem("")
        self.combo_resolution.addItem("")
        self.combo_resolution.addItem("")
        self.combo_resolution.addItem("")
        self.combo_resolution.setObjectName(u"combo_resolution")

        self.horizontalLayout_4.addWidget(self.combo_resolution)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.coord_label = QLabel(self.centralwidget)
        self.coord_label.setObjectName(u"coord_label")
        self.coord_label.setMinimumSize(QSize(180, 0))

        self.horizontalLayout.addWidget(self.coord_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_home = QPushButton(self.centralwidget)
        self.button_home.setObjectName(u"button_home")

        self.horizontalLayout.addWidget(self.button_home)

        self.button_back = QPushButton(self.centralwidget)
        self.button_back.setObjectName(u"button_back")

        self.horizontalLayout.addWidget(self.button_back)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(1, 100)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Device", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.combo_resolution.setItemText(0, QCoreApplication.translate("MainWindow", u"default", None))
        self.combo_resolution.setItemText(1, QCoreApplication.translate("MainWindow", u"1080x1920", None))
        self.combo_resolution.setItemText(2, QCoreApplication.translate("MainWindow", u"1440x2560", None))
        self.combo_resolution.setItemText(3, QCoreApplication.translate("MainWindow", u"1206x2622", None))
        self.combo_resolution.setItemText(4, QCoreApplication.translate("MainWindow", u"1080x2340", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"\n"
"                                                <html><head/><body><p><span\n"
"                                                style=\"\n"
"                                                font-size:20pt;\">Loading</span></p></body></html>", None))
        self.coord_label.setText(QCoreApplication.translate("MainWindow", u"coord_label", None))
        self.button_home.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.button_back.setText(QCoreApplication.translate("MainWindow", u"BACK", None))
    # retranslateUi

