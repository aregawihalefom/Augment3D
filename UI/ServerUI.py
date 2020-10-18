import sys

# import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QVBoxLayout, QSlider, QGridLayout, QGroupBox


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        # set main window attributes
        self.title = 'Augmented Reality'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 800

        # extra parameters
        self.filePath = None
        self.image_label = QLabel('Control settings', self)

        # menu bar for file
        self.menuBar = self.menuBar().addMenu('File')
        self.actionExit = self.menuBar.addAction('Exit')

        # initialize the app
        self.initUI()

    def initUI(self):
        # window location and title
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create menu bar to put some menu Options
        # self.action = self.menuBar.addAction('Open File')
        # self.action.setShortcut('Ctrl+O')
        # self.action.triggered.connect(self.openFileNamesDialog)

        # add exit option to exit the program(keyboard shortcut ctrl+q)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.triggered.connect(self.exitApp)

        # organize UI components
        sliderGroupBox = self.group_sliders()
        self.final_layout(sliderGroupBox)
        self.show()

    def group_sliders(self):
        girdLayout = QGridLayout()
        sliderGroupBox = QGroupBox("Properties")

        sliderGroupBox.setMaximumHeight(500)

        # luminance and contrast
        contrast = QLabel("Contrast", self)
        lumin = QLabel("Luminance", self)

        newfont = QtGui.QFont("Times", 10, QtGui.QFont.Bold)
        contrast.setFont(newfont)
        lumin.setFont(newfont)

        girdLayout.addWidget(contrast, 4, 0)
        girdLayout.addWidget(lumin, 6, 0)
        sliderGroupBox.setLayout(girdLayout)
        return sliderGroupBox

    def final_layout(self, sliderGroupBox):

        hbox = QVBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.image_label)
        hbox.addWidget(sliderGroupBox)
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(hbox)

    # to open file manager
    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "QtWidgets.QFileDialog.getOpenFileNames()",
            "", "Dicom Files (*.*)", options=options)
        if files:
            self.filePath = files[0]
            # go ahead and read the file if necessary

    # will exit the application
    def exitApp(self):
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
