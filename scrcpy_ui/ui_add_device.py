# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_deivce.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_AddDeviceWindow(object):
    def setupUi(self, AddDeviceWindow):
        if not AddDeviceWindow.objectName():
            AddDeviceWindow.setObjectName(u"AddDeviceWindow")
        AddDeviceWindow.resize(294, 257)
        self.horizontalLayout = QHBoxLayout(AddDeviceWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
#ifndef Q_OS_MAC
        self.verticalLayout.setSpacing(-1)
#endif
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.name = QLabel(AddDeviceWindow)
        self.name.setObjectName(u"name")
        self.name.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_2.addWidget(self.name)

        self.nameEdit = QLineEdit(AddDeviceWindow)
        self.nameEdit.setObjectName(u"nameEdit")

        self.horizontalLayout_2.addWidget(self.nameEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.serial = QLabel(AddDeviceWindow)
        self.serial.setObjectName(u"serial")
        self.serial.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_3.addWidget(self.serial)

        self.serialEdit = QLineEdit(AddDeviceWindow)
        self.serialEdit.setObjectName(u"serialEdit")

        self.horizontalLayout_3.addWidget(self.serialEdit)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tunnel = QLabel(AddDeviceWindow)
        self.tunnel.setObjectName(u"tunnel")
        self.tunnel.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_4.addWidget(self.tunnel)

        self.tunnelEdit = QLineEdit(AddDeviceWindow)
        self.tunnelEdit.setObjectName(u"tunnelEdit")

        self.horizontalLayout_4.addWidget(self.tunnelEdit)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.okButton = QPushButton(AddDeviceWindow)
        self.okButton.setObjectName(u"okButton")

        self.horizontalLayout_5.addWidget(self.okButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(AddDeviceWindow)

        QMetaObject.connectSlotsByName(AddDeviceWindow)
    # setupUi

    def retranslateUi(self, AddDeviceWindow):
        AddDeviceWindow.setWindowTitle(QCoreApplication.translate("AddDeviceWindow", u"Dialog", None))
        self.name.setText(QCoreApplication.translate("AddDeviceWindow", u"name", None))
        self.serial.setText(QCoreApplication.translate("AddDeviceWindow", u"serial", None))
        self.tunnel.setText(QCoreApplication.translate("AddDeviceWindow", u"tunnel", None))
        self.okButton.setText(QCoreApplication.translate("AddDeviceWindow", u"OK", None))
    # retranslateUi

