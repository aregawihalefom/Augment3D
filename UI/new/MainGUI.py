import sys

import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QImage, QIcon, QCursor
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QVBoxLayout, QSlider, QGridLayout, QGroupBox


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        # set main window attributes
        self.title = 'PROJECTION AR'
        self.left = 300
        self.top = 100
        self.width = 1024
        self.height = 900
        self.bold_font = QtGui.QFont("Times", 10, QtGui.QFont.Bold)
        self.video_started = False

        # setting cursor

        # extra parameters
        self.timer = QTimer()
        self.cap = None
        self.filePath = None
        self.cursor = None

        # 1. components of the UI
        self.createUIComponents()

        # 2. menu bar for file
        self.createMenu()

        # 3. Build UI
        self.buildUI()

    def buildUI(self):
        """

        """
        # window location and title
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # group the UI compoents
        buttonGroup = self.groupcomponents()

        # set timer timeout callback function
        self.timer.timeout.connect(self.displayImage)

        #  final layout.. all compoents together
        self.finalUi(buttonGroup)

        # show the UI
        self.show()

    def createUIComponents(self):
        """

        """
        # Main video label
        self.videoLabel = QLabel('Video feed not avaliable , Start video by clicking on the start button on the top '
                                 'left of the tool list', self)
        self.videoLabel.setFont(self.bold_font)

        # Start video button
        self.startVideoButton = QtWidgets.QPushButton(" Strat Video ", self)
        self.startVideoButton.setIcon(QIcon("icons/icons8-start-50.png"))
        self.startVideoButton.clicked.connect(self.startVideo)

        # Pencil tool
        self.pencilButton = QtWidgets.QPushButton(" Draw ", self)
        self.pencilButton.setIcon(QIcon("icons/icons8-pencil-50.png"))
        self.pencilButton.clicked.connect(self.drawUsingPencil)

        # rectangle tool
        self.rectangleButton = QtWidgets.QPushButton(" Select ", self)
        self.rectangleButton.setIcon(QIcon("icons/icons8-rectangle-50.png"))

        # lasso tool
        self.lassoButton = QtWidgets.QPushButton(" Lasso ", self)
        self.lassoButton.setIcon(QIcon("icons/icons8-lasso-tool-48.png"))

        # Stop Video button
        self.stopVideoButton = QtWidgets.QPushButton(" Pause ", self)
        self.stopVideoButton.setIcon(QIcon("icons/icons8-stop-squared-50.png"))
        self.stopVideoButton.clicked.connect(self.stopVideo)

        self.exitButton = QtWidgets.QPushButton(" exit ", self)
        self.exitButton.setIcon(QIcon("icons/icons8-exit-50.png"))
        self.exitButton.clicked.connect(self.exitApp)

        self.change_button_status()

    def createMenu(self):

        """

        """
        self.fileMenuBar = self.menuBar().addMenu('File')
        self.editMenuBar = self.menuBar().addMenu('Edit')

        self.actionExit = self.fileMenuBar.addAction('Exit')
        self.actionOpen = self.fileMenuBar.addAction('Open File')

        # create menu bar to put some menu Options
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(self.openFileNamesDialog)

        # add exit option to exit the program(keyboard shortcut ctrl+q)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.triggered.connect(self.exitApp)

    def groupcomponents(self):

        """

        """
        # create grid layout to group components
        gridLayout = QGridLayout()

        toolsButtonGroupBox = QGroupBox("Tools")
        toolsButtonGroupBox.setToolTip("Tool Box")
        # buttonGroupBox.setMaximumHeight(500)

        # add component to the gridLayout here
        gridLayout.addWidget(self.startVideoButton, 1, 0)
        gridLayout.addWidget(self.stopVideoButton, 1, 1)
        # toolsButtonGroupBox.setLayout(gridLayout)

        # vertical layout
        vLayout = QVBoxLayout()
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.addWidget(self.startVideoButton)
        vLayout.addWidget(self.pencilButton)
        vLayout.addWidget(self.rectangleButton)
        vLayout.addWidget(self.lassoButton)
        vLayout.addWidget(self.stopVideoButton)
        vLayout.addWidget(self.exitButton)

        # set the layout to the button group
        toolsButtonGroupBox.setLayout(vLayout)

        return toolsButtonGroupBox

    def finalUi(self, buttonGroup):
        """

        """
        gridLayout = QGridLayout()

        # add widgets to the layout
        gridLayout.addWidget(buttonGroup, 0, 0)
        gridLayout.addWidget(self.videoLabel, 0, 1, 1, 2)

        # widget for the general layout
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(gridLayout)

    def startVideo(self):
        """

        """
        try:
            # if timer is stopped
            if not self.timer.isActive():
                # create video capture  and start timer
                self.cap = cv2.VideoCapture(2)
                self.videoLabel.setText("Connecting to camera")
                self.video_started = True
                self.change_button_status()
                self.timer.start(10)


        except Exception as ex:
            print(ex)

    def stopVideo(self):
        """

        """
        # if the camera is alraedy started close it
        if self.timer.isActive():
            # close camera
            self.cap.release()
            self.image_label.setText("Camera is closed")

        else:
            self.image_label.setText('Camera is not started')

    def displayImage(self):
        """

        """
        try:
            # read form camera
            ret, image = self.cap.read()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # image = cv2.Canny(image, 70, 120)

            # get image info
            height, width, channel = image.shape
            step = channel * width
            # create QImage from imageQImage::Format_Grayscale8
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)

            # show image in img_label
            self.videoLabel.setPixmap(QPixmap.fromImage(qImg))
            # call back for drawing
            # cv2.setMouseCallback("Mouse moves", draw_shape)

        except Exception as ex:
            print(ex)

    def drawUsingPencil(self):

        # change the cursor to pencil
        CURSOR_NEW = QtGui.QCursor(QtGui.QPixmap('cursors/icons8-pencil-28.png'))
        self.startVideoButton.setEnabled(False)
        self.setCursor(CURSOR_NEW)
        pass

    def openFileNamesDialog(self):
        """

        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "QtWidgets.QFileDialog.getOpenFileNames()",
            "", "Dicom Files (*.*)", options=options)
        if files:
            self.filePath = files[0]
            # go ahead and read the file if necessary

    def exitApp(self):
        """

        """
        sys.exit(0)

    def change_button_status(self):
        """

        """
        if not self.video_started:
            self.stopVideoButton.setEnabled(False)
            self.pencilButton.setEnabled(False)
            self.rectangleButton.setEnabled(False)
            self.lassoButton.setEnabled(False)
            self.startVideoButton.setEnabled(True)

        else:
            self.startVideoButton.setEnabled(False)
            self.stopVideoButton.setEnabled(True)
            self.pencilButton.setEnabled(True)
            self.lassoButton.setEnabled(True)
            self.rectangleButton.setEnabled(True)


class Events:

    def __init__(self):
        pass


draw = xi = yi = new_line = xi_backup = yi_backup = 0


# mouse callback function
def draw_shape(event, x, y, flags, param):
    global draw, xi, yi, new_line, xi_backup, yi_backup
    if event == cv2.EVENT_LBUTTONDOWN:
        draw = True
        xi.append(x)
        yi.append(y)
    # new_line += 1

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw:
            xi.append(x)
            yi.append(y)

    elif event == cv2.EVENT_LBUTTONUP:
        xi.append(-4)
        yi.append(-4)
        new_line += 1
        draw = False

    elif event == cv2.EVENT_MOUSEWHEEL:
        xi_backup, yi_backup = xi, yi
        print(xi_backup)
        print("Cleared Mouse event")
        xi.clear()
        yi.clear()
        new_line = 0
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        print("Button double clicked")
        xi, yi = xi_backup, yi_backup


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
