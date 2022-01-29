# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
from PySide2.QtGui import QPixmap
from PySide6.QtCore import Slot
import cv2


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.open_pic)
        self.label = QLabel()
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QVBoxLayout()
    #    layout.addWidget(self.edit)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
#        self.openFileNameDialog()
#        self.openFileNamesDialog()
#        self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    # Greetings

    @Slot()
    def open_pic(self):
        fileName = self.openFileNameDialog()
        img = cv2.imread(fileName)
        cv2.imshow('123', img)
        self.pixmap = QPixmap(fileName)
        self.label.setPixmap(self.pixmap)
        print(fileName)

if __name__ == "__main__":
    app = QApplication([])
#    fileName = QFileDialog.getOpenFileName(self,
#        tr("Open Image"), "/home/jana", tr("Image Files (*.png *.jpg *.bmp)"))
    # Show the button
    # button.show()
    window = Widget()

    # Create a button
    # Connect the button to the function





#    window.show()
    sys.exit(app.exec_())
