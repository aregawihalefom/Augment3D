import sys

import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QIcon, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QVBoxLayout, QSlider, QGridLayout, QGroupBox


# this UI serve as image display window for projector
class PhotoToProjector(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Secondary Window")
        self.label.setAttribute(Qt.WA_TranslucentBackground, True)

        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setStyleSheet("background:transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showMaximized()


# this UI serve as main window to draw the annotation
class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        # set main window attributes
        self.title = 'PROJECTION AR'
        self.left = 300
        self.top = 100
        # self.width = 1400
        # self.height = 900
        self.sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        # print(sizeObject.height(), sizeObject.height())
        self.secondaryWindow = PhotoToProjector()
        # self.video_height = 720
        # self.video_width = 1280
        self.bold_font = QtGui.QFont("Times", 10, QtGui.QFont.Bold)
        self.video_started = False
        self.pencil_started = False

        # extra parameters
        self.timer = QTimer()
        self.cap = None
        self.filePath = None
        self.cursor = None

        # variable for annotation
        self.draw_pixmap = QPixmap(self.sizeObject.width()-20, self.sizeObject.height()-100)
        self.draw_pixmap.fill(Qt.transparent)
        self.painter = QPainter(self.draw_pixmap)
        self.annotation_label = QLabel(self)

        # custom drawing variables
        self.drawing = False
        self.brushSize = 6
        self.brushColor = Qt.green
        self.lastPoint = QPoint()

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
        # self.setGeometry(self.left, self.top, self.width(), self.height())
        self.setWindowIcon(QIcon("icons/icon-green.png"))
        self.showMaximized()

        # group the UI components
        # buttonGroup = self.groupcomponents()

        #  final layout.. all compoents together
        self.finalUi()


        # show the UI
        self.show()
        # create second window
        self.secondaryWindow.show()

    def createUIComponents(self):
        """

        """
        # Main video label
        self.videoLabel = QLabel('Start Video', self)
        self.videoLabel.setFont(self.bold_font)
        self.videoLabel.setStyleSheet("border: 1px solid black;")
        # self.change_button_status()

    def createMenu(self):
        """  Create and add menu items into menu bar

        """
        self.fileMenuBar = self.menuBar().addMenu('File')
        self.editMenuBar = self.menuBar().addMenu('Edit')

        self.startVideoButton = self.fileMenuBar.addAction(" Strat Video")
        self.actionExit = self.fileMenuBar.addAction('Exit')
        self.actionOpen = self.fileMenuBar.addAction('Open File')

        self.pencilButton = self.editMenuBar.addAction("Draw")
        self.stopVideoButton = self.editMenuBar.addAction("Pause")
        self.lassoButton = self.editMenuBar.addAction("Lasso")
        self.rectangleButton = self.editMenuBar.addAction("Select")

        # Pencil tool
        self.pencilButton.setIcon(QIcon("icons/icons8-pencil-50.png"))
        self.pencilButton.triggered.connect(self.drawUsingPencil)

        # rectangle tool
        self.rectangleButton.setIcon(QIcon("icons/icons8-rectangle-50.png"))

        # lasso tool
        self.lassoButton.setShortcut("Ctrl+L")
        self.lassoButton.setIcon(QIcon("icons/icons8-lasso-tool-48.png"))

        # Stop Video button
        self.stopVideoButton.setShortcut('Ctrl+P')
        self.stopVideoButton.setIcon(QIcon("icons/icons8-stop-squared-50.png"))
        self.stopVideoButton.triggered.connect(self.stopVideo)

        # start button
        self.startVideoButton.setShortcut('Ctrl+S')
        self.startVideoButton.setIcon(QIcon("icons/icons8-start-50.png"))
        self.startVideoButton.triggered.connect(self.startVideo)

        # create menu bar to put some menu Options
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(self.openFileNamesDialog)

        # add exit option to exit the program(keyboard shortcut ctrl+q)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.setIcon(QIcon("icons/icons8-exit-50.png"))
        self.actionExit.triggered.connect(self.exitApp)

    # def groupcomponents(self):
    #
    #     """
    #
    #     """
    #     # create grid layout to group components
    #     gridLayout = QGridLayout()
    #
    #     toolsButtonGroupBox = QGroupBox("Tools")
    #     toolsButtonGroupBox.setToolTip("Tool Box")
    #     toolsButtonGroupBox
    #     # buttonGroupBox.setMaximumHeight(500)
    #
    #     # add component to the gridLayout here
    #     gridLayout.addWidget(self.startVideoButton, 1, 0)
    #     gridLayout.addWidget(self.stopVideoButton, 1, 1)
    #     # toolsButtonGroupBox.setLayout(gridLayout)
    #
    #     # vertical layout
    #     vLayout = QVBoxLayout()
    #     vLayout.setSpacing(0)
    #     vLayout.setContentsMargins(0, 0, 0, 0)
    #     vLayout.addWidget(self.startVideoButton)
    #     vLayout.addWidget(self.pencilButton)
    #     vLayout.addWidget(self.rectangleButton)
    #     vLayout.addWidget(self.lassoButton)
    #     vLayout.addWidget(self.stopVideoButton)
    #     vLayout.addWidget(self.exitButton)
    #
    #     # set the layout to the button group
    #     toolsButtonGroupBox.setLayout(vLayout)
    #
    #     return toolsButtonGroupBox

    def finalUi(self):
        """

        """
        gridLayout = QGridLayout()

        # add widgets to the layout
        # gridLayout.addWidget(buttonGroup, 0, 0)
        gridLayout.addWidget(self.videoLabel, 0, 1, 1, 8)
        gridLayout.addWidget(self.annotation_label, 0, 1, 1, 8)

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
                self.cap = cv2.VideoCapture(0)

                self.videoLabel.setText("Connecting to camera")
                self.video_started = True
                # self.change_button_status()
                # set timer timeout callback function
                self.timer.timeout.connect(self.displayImage)
                self.timer.start(100)

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
            image = cv2.resize(image, (self.sizeObject.width()-20, self.sizeObject.height()-100))
            # image = cv2.Canny(image, 70, 120)

            # get image info
            height, width, channel = image.shape
            # print(width, height)
            step = channel * width

            # create QImage from imageQImage::Format_Grayscale8
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)

            # show image in img_label
            self.videoLabel.setPixmap(QPixmap.fromImage(qImg))

        except Exception as ex:
            print(ex)

    def drawUsingPencil(self):

        # change the cursor to pencil
        CURSOR_NEW = QtGui.QCursor(QtGui.QPixmap('cursors/icons8-pencil-28.png'))
        self.startVideoButton.setEnabled(False)
        self.setCursor(CURSOR_NEW)
        self.drawing = True

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
    #
    # def change_button_status(self):
    #     """
    #
    #     """
    #     if not self.video_started:
    #         self.stopVideoButton.setEnabled(False)
    #         self.pencilButton.setEnabled(False)
    #         self.rectangleButton.setEnabled(False)
    #         self.lassoButton.setEnabled(False)
    #         self.startVideoButton.setEnabled(True)
    #
    #     else:
    #         self.startVideoButton.setEnabled(False)
    #         self.stopVideoButton.setEnabled(True)
    #         self.pencilButton.setEnabled(True)
    #         self.lassoButton.setEnabled(True)
    #         self.rectangleButton.setEnabled(True)

    # add different events
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):

        if (event.buttons() & Qt.LeftButton) & self.drawing and self.rect().contains(event.pos()):
            self.painter.setOpacity(0.9)
            self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.painter.drawLine(self.lastPoint, event.pos() )
            self.annotation_label.setPixmap(self.draw_pixmap)
            self.lastPoint = event.pos()

            # update secondary window image
            self.secondaryWindow.label.setPixmap(self.draw_pixmap)
            self.secondaryWindow.label.resize(self.secondaryWindow.width(), self.secondaryWindow.height())
            self.update()

    # highlight
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.save()

    def save(self):
        try:
            filePath = 'annotation.png'
            self.draw_pixmap.save(filePath)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        sys.exit(app.exec_())
    except Exception as ex:
        print(ex)
