# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\resources\ui\widget_image.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WidgetLog(object):

    def setupUi(self, WidgetImage):
        WidgetImage.setObjectName("WidgetImage")
        WidgetImage.resize(857, 781)
        self.gridLayout = QtWidgets.QGridLayout(WidgetImage)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBar = QtWidgets.QProgressBar(WidgetImage)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(WidgetImage)
        self.frame.setStyleSheet("background-color: rgb(173, 211,230);\n"
"border: 2px solid black;\n"
"border-radius: 6px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("background: black")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.frame)
        self.scrollArea.setMaximumSize(QtCore.QSize(300, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 246, 698))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("V_Layout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(WidgetImage)
        QtCore.QMetaObject.connectSlotsByName(WidgetImage)

    def retranslateUi(self, WidgetImage):
        _translate = QtCore.QCoreApplication.translate
        WidgetImage.setWindowTitle(_translate("WidgetImage", "Form"))
        self.label.setText(_translate("WidgetImage", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WidgetImage = QtWidgets.QWidget()
    ui = Ui_WidgetImage()
    ui.setupUi(WidgetImage)
    WidgetImage.show()
    sys.exit(app.exec_())
