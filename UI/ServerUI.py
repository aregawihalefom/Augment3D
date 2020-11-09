import sys
import numpy as np
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QVBoxLayout, QSlider, QGridLayout, QGroupBox

# for debugging purpose
import traceback


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        # set main window attributes
        self.title = 'Augmented Reality'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 400

        # -------------------- annotation parameters  -------------------
        self.annotation_image = QImage(self.size(), QImage.Format_RGB32)
        self.annotation_image.fill(Qt.transparent)

        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.green
        self.lastPoint = QPoint()

        # extra parameters
        self.timer = QTimer()
        self.cap = None
        self.filePath = None
        self.image_label = QLabel('Video to be shown where', self)
        self.start_video_button = QtWidgets.QPushButton('Start', self)
        self.stop_video_button = QtWidgets.QPushButton('Stop', self)
        self.bold_font = QtGui.QFont("Times", 10, QtGui.QFont.Bold)

        # menu bar for file
        self.menuBar = self.menuBar().addMenu('File')
        self.actionExit = self.menuBar.addAction('Exit')
        self.actionOpen = self.menuBar.addAction('Open File')

        # initialize the app
        self.initUI()

    # initialize application window with components
    def initUI(self):
        # window location and title
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create menu bar to put some menu Options
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(self.openFileNamesDialog)

        # add exit option to exit the program(keyboard shortcut ctrl+q)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.triggered.connect(self.exitApp)

        # set timer timeout callback function
        self.timer.timeout.connect(self.display_image)

        # organize UI components
        groupBox = self.group_components()
        self.final_layout(groupBox)
        self.show()

    # to group components on the main window
    def group_components(self):
        # create grid layout to group components
        gridLayout = QGridLayout()
        buttonGroupBox = QGroupBox("Properties")
        buttonGroupBox.setMaximumHeight(500)

        # setup buttons to control video
        self.start_video_button.clicked.connect(self.start_video)
        self.start_video_button.setFont(self.bold_font)
        self.stop_video_button.clicked.connect(self.stop_video)
        self.stop_video_button.setFont(self.bold_font)

        # add component to the gridLayout here
        gridLayout.addWidget(self.start_video_button, 1, 0)
        gridLayout.addWidget(self.stop_video_button, 1, 1)
        buttonGroupBox.setLayout(gridLayout)
        return buttonGroupBox

    # arrange the video and the other components in box layout
    def final_layout(self, groupBox):
        # create vertical box and add elements
        vertical_box = QVBoxLayout()
        vertical_box.addStretch(1)
        vertical_box.addWidget(self.image_label)
        vertical_box.addWidget(groupBox)

        # widget to put the box layout created
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vertical_box)

    # start display camera feed on the image label
    def start_video(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture  and start timer
            self.cap = cv2.VideoCapture(0)
            self.timer.start(10)

    # stop displaying camera feed to the image label
    def stop_video(self):
        # if the camera is alraedy started close it
        if self.timer.isActive():
            # close camera
            self.cap.release()
            self.image_label.setText("Camera is closed")
            self.timer.stop()

        # else:
        #     self.image_label.setText('Camera is not started')

    # display image to label
    def display_image(self):
        try:
            # read form camera
            ret, image = self.cap.read()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # get image info
            height, width, channel = image.shape
            step = channel * width

            # overlay annotation on to video feed
            qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)

            painterInstance = QtGui.QPainter()
            painterInstance.begin(qImg)
            painterInstance.drawImage(0,0, self.annotation_image)
            painterInstance.end()

            # create QImage and show image on img_label
            self.image_label.setPixmap(QPixmap.fromImage(qImg))

        except Exception as e:
            traceback.print_exc()

    # to open file manager
    def openFileNamesDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog

        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "QtWidgets.QFileDialog.getOpenFileNames()",
            "", "Dicom Files (*.*)", options=options)
        if files:
            self.filePath = files[0]
            # TODO:
            # get file resource

    # will exit the application
    def exitApp(self):
        sys.exit(0)

    # --------------- annotation drawing stuff -------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.annotation_image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.save()

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.annotation_image, self.annotation_image.rect())

    def save(self):
        filePath = 'annotation.png'
        self.annotation_image.save(filePath)

    # --------------------- anootaion end here ---------------------


# execute everything
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
