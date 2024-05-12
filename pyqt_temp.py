import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QMainWindow, QPushButton, QLineEdit


class MyWindow(QMainWindow):

    def update_text(self):
        a = self.input_field.text()
        ans = eval(a)
        self.textLabel.setText(str(ans))

    def __init__(self):
        QMainWindow.__init__(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid = QGridLayout()
        central_widget.setLayout(grid)
        self.input_field = QLineEdit()
        grid.addWidget(self.input_field, 1, 0)

        self.textLabel = QLabel()
        self.textLabel.setText("")
        grid.addWidget(self.textLabel, 2, 1)
        self.textLabel.setAlignment(Qt.AlignCenter)

        self.textLabe0 = QLabel()
        self.textLabe0.setText("ответ")
        grid.addWidget(self.textLabe0, 2, 0)
        self.textLabe0.setAlignment(Qt.AlignCenter)

        button = QPushButton('решить')
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 1, 1)

        self.setGeometry(50, 50, 600, 200)
        self.setWindowTitle("PyQt Example")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
