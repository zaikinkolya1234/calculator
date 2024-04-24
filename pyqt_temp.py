import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QMainWindow, QPushButton, QLineEdit


class MyWindow(QMainWindow):

    def update_text(self):
        self.textLabel.setText(self.input_field.text())

    def __init__(self):
        QMainWindow.__init__(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid = QGridLayout()
        central_widget.setLayout(grid)
        self.input_field = QLineEdit()
        grid.addWidget(self.input_field, 0, 0)

        self.textLabel = QLabel()
        self.textLabel.setText("Hello World!")
        grid.addWidget(self.textLabel, 0, 1)
        self.textLabel.setAlignment(Qt.AlignCenter)

        button = QPushButton('обновить')
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 0, 2)

        self.setGeometry(50, 50, 600, 200)
        self.setWindowTitle("PyQt Example")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
