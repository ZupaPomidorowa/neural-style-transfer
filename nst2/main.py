import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QFileDialog

import matplotlib.pylab as plt
from API import transfer_style


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('NST')
        self.setGeometry(100, 100, 500, 300)

        self.content_image_path = None
        self.style_image_path = None

        title = QLabel('Neural Style Transformer Application', self)
        title.setAlignment(Qt.AlignCenter)

        self.image1 = QLabel(self)
        pixmap1 = QPixmap('image1.jpg').scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image1.setPixmap(pixmap1)
        self.image1.setAlignment(Qt.AlignCenter)

        self.image2 = QLabel(self)
        pixmap2 = QPixmap('monet.jpg').scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image2.setPixmap(pixmap2)
        self.image2.setAlignment(Qt.AlignCenter)

        label1 = QLabel('Content image', self)
        label1.setAlignment(Qt.AlignCenter)
        button1 = QPushButton('Upload', self)
        button1.setFixedSize(200, 30)
        button1.clicked.connect(self.upload_image1)

        label2 = QLabel('Style image', self)
        label2.setAlignment(Qt.AlignCenter)
        button2 = QPushButton('Upload', self)
        button2.setFixedSize(200, 30)
        button2.clicked.connect(self.upload_image2)

        images_layout = QGridLayout()
        images_layout.addWidget(label1, 0, 0)
        images_layout.addWidget(button1, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        images_layout.addWidget(self.image1, 2, 0)
        images_layout.addWidget(label2, 0, 1)
        images_layout.addWidget(button2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        images_layout.addWidget(self.image2, 2, 1)

        button3 = QPushButton('Generate', self)
        button3.setFixedSize(200, 30)
        button3.clicked.connect(self.generate_image)
        button4 = QPushButton('Save', self)
        button4.setFixedSize(200, 30)
        button4.clicked.connect(self.save_image)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(button3)
        buttons_layout.addWidget(button4)

        self.generated_image = QLabel(self)
        pixmap3 = QPixmap('image3.jpg').scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.generated_image.setPixmap(pixmap3)
        self.generated_image.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(images_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.generated_image)

        self.setLayout(main_layout)

    def upload_image1(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Image files (*.jpg *.png)")
        file_dialog.setWindowTitle("Upload Content Image")
        if file_dialog.exec_():
            self.content_image_path= file_dialog.selectedFiles()[0]
            pixmap1 = QPixmap(self.content_image_path).scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image1.setPixmap(pixmap1)
            print(self.content_image_path)

    def upload_image2(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Image files (*.jpg *.png)")
        file_dialog.setWindowTitle("Upload Content Image")
        if file_dialog.exec_():
            self.style_image_path = file_dialog.selectedFiles()[0]
            pixmap2 = QPixmap(self.style_image_path).scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image2.setPixmap(pixmap2)
            print(self.style_image_path)

    def generate_image(self):
        model_path = r"/home/daria/Neural-Style-Transfer/model"
        img = transfer_style(self.content_image_path, self.style_image_path, model_path)
        plt.imsave('stylized_image.jpeg', img)
        pixmap3 = QPixmap('stylized_image.jpeg').scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.generated_image.setPixmap(pixmap3)

    def save_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(".jpg")
        file_dialog.setNameFilter("JPEG Image (*.jpg);;PNG Image (*.png)")
        file_dialog.setWindowTitle("Save Generated Image")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            pixmap3 = self.generated_image.pixmap()
            pixmap3.save(selected_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
