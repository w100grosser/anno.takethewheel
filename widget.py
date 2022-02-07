# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
from PySide2.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from PySide2.QtGui import QMouseEvent
from PySide6.QtCore import Slot
from PySide6.QtCore import QUrl, Qt, QEvent, QTimer, QRect, QPoint
import cv2
import os
import ast


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.points = {}
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.button = QPushButton("Choose images folder")
        self.button.clicked.connect(self.open_pic_folder)
        self.button1 = QPushButton("Next Image")
        self.button1.clicked.connect(self.next_im)
        self.button2 = QPushButton("Save Images")
        self.button2.clicked.connect(self.save_ims)
        self.button2 = QPushButton("Previous Image")
        self.button2.clicked.connect(self.prev_im)
        self.label = QLabel()
        self.label1 = QLabel()
        self.current_image_path = ""
        self.image_paths = []
        self.pen = QPen()
        self.pen.setWidth(10)
        self.pen.setColor(QColor(168, 34, 3))
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QVBoxLayout()
    #    layout.addWidget(self.edit)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label1)
        self.setLayout(self.layout)
#        self.openFileNameDialog()
#        self.openFileNamesDialog()
#        self.saveFileDialog()

        self.show()

#    def openFileNameDialog(self):
#        options = QFileDialog.Options()

#        options |= QFileDialog.DontUseNativeDialog
##        fileName, _ = QFileDialog.get
#        dialog = QFileDialog()
#        fileName, _ = dialog.getOpenFileName(self , options=options)
##        fileName, _ = QFileDialog.getOpenFileName(self , options=options)
#        if fileName:
#            print(fileName)
#            return fileName

    def openFileNameDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
#        fileName, _ = QFileDialog.get
        dialog = QFileDialog()
        dir_path=QFileDialog.getExistingDirectory(self,"Choose Directory")
        if dir_path:
            print(dir_path)
            return dir_path

#    def openFolderNameDialog(self):
#        options = QFolderDialog.Options()
#        FolderName, _ = QFolderDialog.getOpenFolderName(self, options=options)
#        if FolderName:
#            print(FolderName)
#            return FolderName

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

    def mouseMoveEvent(self, event):
        self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
            if len(self.points[self.current_image_path]) < 5:
                self.points[self.current_image_path].append((event.x() - self.label1.x(), event.y() - self.label1.y()))
                canvas = self.label1.pixmap()
                painter = QPainter(canvas)
                painter.setPen(self.pen)
#                painter.drawLine(event.x() - self.label1.x(), event.y() - self.label1.y(), 300, 200)
                painter.drawPoint(event.x() - self.label1.x(), event.y() - self.label1.y())
                painter.end()
                self.label1.setPixmap(canvas)

    def keyPressEvent(self, event):
#        if event.type() == QEvent.KeyPress:
        print('event received @ myDialog')
        if event.key() == Qt.Key_R:
            self.points[self.current_image_path] = []
            self.pixmap = QPixmap(self.current_image_path)
            self.label1.setPixmap(self.pixmap)
            print(0)

        if event.key() == Qt.Key_E:
            self.next_im()

        if event.key() == Qt.Key_Q:
            self.prev_im()

        if event.key() == Qt.Key_S:
            self.save_ims()
    # Greetings

    @Slot()
    def open_pic_file(self, fileName):
#        fileName = self.openFolderNameDialog()
        self.current_image_path = fileName
        self.img = cv2.imread(self.current_image_path)
        self.pixmap = QPixmap(self.current_image_path)
        self.label1.setPixmap(self.pixmap)
        self.label1.setMouseTracking(True)
        canvas = self.label1.pixmap()
        painter = QPainter(canvas)
        for p in self.points[self.current_image_path]:
            painter.setPen(self.pen)
        #            painter.drawLine(event.x() - self.label1.x(), event.y() - self.label1.y(), 300, 200)
            painter.drawPoint(p[0], p[1])
        painter.end()
        print(self.current_image_path, self.file_number, self.points[self.current_image_path])

    @Slot()
    def open_pic(self):
        fileName = self.openFileNameDialog()
        self.open_pic_file(fileName)

    @Slot()
    def next_im(self):
        if self.file_number < len(self.image_paths) - 1:
            self.file_number += 1
            self.open_pic_file(self.image_paths[self.file_number])

    @Slot()
    def save_ims(self):
        with open(self.current_folder_path + "/CACHE.txt","w") as f:
            points_str = []
            for file in self.points.keys():
                points_str.append(file.split('/')[-1] + '\t' + str(self.points[file]))
            f.write('\n'.join(points_str))


    @Slot()
    def prev_im(self):
        if self.file_number > 0:
            self.file_number -= 1
            self.open_pic_file(self.image_paths[self.file_number])

    def open_pic_folder(self):
        self.file_number = 0
        folderName = self.openFileNameDialog()
#        fileName = self.openFolderNameDialog()
        self.current_folder_path = folderName
#        self.image_paths.append(self.current_folder_path)
        print(self.current_folder_path)
        files = os.listdir(self.current_folder_path)
        cache_exists = 0
        if 'CACHE.txt' in  files:
            with open(self.current_folder_path + "/CACHE.txt", "r") as cache:
                cache_exists = 1
                for line in cache.read().split('\n'):
                    self.points[self.current_folder_path + '/' + line.split('\t')[0]] = ast.literal_eval(line.split('\t')[1])
        for f in files:
            if '.png' in f or '.jpg' in f:
                self.image_paths.append(self.current_folder_path + '/' + f)
                if cache_exists == 0:
                    self.points[self.image_paths[-1]] = []
        if len(self.image_paths):
            self.open_pic_file(self.image_paths[self.file_number])






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
