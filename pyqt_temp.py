import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QMainWindow, QPushButton


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid = QGridLayout()
        central_widget.setLayout(grid)
        textLabel = QLabel()
        textLabel.setText("Hello World!")
        grid.addWidget(textLabel, 0, 0)
        textLabel.setAlignment(Qt.AlignCenter)

        button = QPushButton('Push me!')
        button.clicked.connect(lambda x: print('You pushed me!'))
        grid.addWidget(button, 0, 1)

        self.setGeometry(50, 50, 300, 100)
        self.setWindowTitle("PyQt Example")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
