import re
import sys
from math import sin, cos, tan, pi
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QMainWindow, QPushButton, QLineEdit, QFrame, \
    QAction, QToolBar, QMenuBar


class MyWindow(QMainWindow):

    def update_text(self):
        """
        обновляет текстовое поле с проверкой
        :return: None
        """

        if self.flagans:
            self.input_field.setText('')
            self.flagans = False

        s = self.input_field.text()

        if len(s) == 0:
            if self.sender().text() in '*+-/mod^':
                return

        if self.sender().text() == 'pi':
            if len(s) != 0 and s[-1] in '1234567890.':
                return

        if self.sender().text() in '1234567890.':
            if len(s) != 0 and s[-1] in 'pi':
                return

        if self.sender().text() == 'mod':
            if len(s) != 0 and s[-1] not in '1234567890)' or len(s) == 0:
                return

        if self.sender().text() == 'sin' or self.sender().text() == 'cos' or self.sender().text() == 'tan':
            if len(s) != 0 and s[-1] in '123456789)':
                return

        if s.endswith('mod'):
            if self.sender().text() not in '1234567890(':
                return

        floatzero = True
        if len(self.input_field.text()) != 0 and self.sender().text().isdigit():
            if self.input_field.text()[-1] == '0':
                for i in range(len(self.input_field.text()) - 1, -1, -1):
                    if self.input_field.text()[i] == '.':
                        break
                    if not self.input_field.text()[i].isdigit() or i == 0:
                        floatzero = False
                        self.input_field.setText(self.input_field.text()[:-1] + self.sender().text())
        if self.sender().text() == '.':
            if len(self.input_field.text()) == 0:
                return
            if not self.input_field.text()[-1].isdigit():
                return
            for i in range(len(self.input_field.text()) - 1, 0, -1):
                if self.input_field.text()[i] == '.':
                    return
                if self.input_field.text()[i] in self.st:
                    break
        if floatzero:
            a = self.input_field.text() + self.sender().text()
            self.input_field.setText(a)

    def getans(self):
        self.flagans = True
        try:
            s = self.input_field.text()
            s = s.replace('^', '**').replace('mod', '%')
            functions = {'sin': sin, 'cos': cos, 'tan': tan}
            for trigonometry in self.st2:
                while trigonometry in s:
                    i = s.index(trigonometry)
                    line = ''
                    for j in range(i + 4, len(s)):
                        if s[j] == ')':
                            break
                        line += s[j]
                    assert self.checkcorrect(line)

                    s = s[:i] + str(functions[trigonometry](eval(line))) + s[j + 1:]
            assert self.checkcorrect(s)
            self.input_field.setText(str(eval(s)))
        except AssertionError:
            self.input_field.setText("неправильный ввод")
        except ZeroDivisionError:
            self.input_field.setText("нельзя делить на ноль")
        except Exception:
            self.input_field.setText('некорректный ввод')

    def checkcorrect(self, s):
        if (re.search(r'[+\-*/]{2}', s) and '**' not in s) or re.search(r'\d\(', s) or re.search(r'\)\d',
                                                                                                 s) or '()' in s or ')(' in s or \
                re.search(r'[+\-*/]\)', s) or re.search(r'\([+*/]', s) or s.count('(') != s.count(')') or \
                re.search(r'sin^\(', s) or re.search(r'cos^\(', s) or re.search(r'tan^\(', s):
            return False
        return True

    def backspace(self):
        self.input_field.setText(self.input_field.text()[:-1])

    def reset(self):
        self.flagans = True
        self.input_field.setText('')

    def increase(self):
        try:
            a = float(self.input_field.text())
        except Exception:
            return
        if '.' in self.input_field.text():
            a = self.input_field.text() + '0'
            self.input_field.setText(a)
        else:
            a = self.input_field.text() + '.0'
            self.input_field.setText(a)

    def reduce(self):
        try:
            a = float(self.input_field.text())
        except Exception:
            return
        if '.' in self.input_field.text():
            a = self.input_field.text()[:-1]
            if self.input_field.text()[-2] == '.':
                a = self.input_field.text()[:-2]

            self.input_field.setText(a)
        else:
            return

    def engineer(self, flag=False):
        flagqframe = False
        for i in self.central_widget.children():
            if flagqframe:
                if isinstance(i, QPushButton):
                    i.setEnabled(flag)
            if isinstance(i, QFrame):
                flagqframe = True

    def __init__(self):
        super().__init__()

        menubar = QMenuBar()
        file_menu = menubar.addMenu('настройки')

        engineer_actionon = QAction('включить инженерный режим', self)
        engineer_actionon.triggered.connect(lambda: self.engineer(True))
        file_menu.addAction(engineer_actionon)

        engineer_actionoff = QAction('выключить инженерный режим', self)
        engineer_actionoff.triggered.connect(lambda: self.engineer(False))
        file_menu.addAction(engineer_actionoff)

        self.flagans = False
        QMainWindow.__init__(self)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        grid = QGridLayout()
        self.central_widget.setLayout(grid)
        grid.setMenuBar(menubar)
        self.input_field = QLineEdit()
        self.input_field.setReadOnly(True)
        grid.addWidget(self.input_field, 0, 0, 1, 4)

        ##button.clicked.connect(self.update_text)

        for i in range(3):
            for j in range(3):
                if 0 < i * 3 + j + 1 < 10:
                    button = QPushButton(str(i * 3 + j + 1))
                    button.setProperty("class", 'digit')
                    button.clicked.connect(self.update_text)
                    grid.addWidget(button, i + 1, j)

        self.st = ('+', '-', '*', '/')
        for i in range(4):
            button = QPushButton(str(self.st[i]))
            button.clicked.connect(self.update_text)
            grid.addWidget(button, i + 1, 3)

        button = QPushButton("del")
        button.clicked.connect(self.backspace)
        grid.addWidget(button, 4, 0)

        button = QPushButton(str(0))
        button.setProperty("class", 'digit')
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 4, 1)

        button = QPushButton("=")
        button.clicked.connect(self.getans)
        grid.addWidget(button, 4, 2)

        button = QPushButton("C")
        button.clicked.connect(self.reset)
        grid.addWidget(button, 5, 0)

        button = QPushButton('(')
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 5, 1)

        button = QPushButton(')')
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 5, 2)

        button = QPushButton(".")
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 5, 3)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        grid.addWidget(line, 6, 0, 1, 4)

        self.st2 = ('sin', 'cos', 'tan')
        for i in range(3):
            button = QPushButton(str(self.st2[i]))
            button.clicked.connect(self.update_text)
            grid.addWidget(button, 7, i)

        button = QPushButton(">")
        button.clicked.connect(self.increase)
        grid.addWidget(button, 7, 3)

        button = QPushButton('pi')
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 8, 0)

        button = QPushButton("mod")
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 8, 1)

        button = QPushButton('^')
        button.clicked.connect(self.update_text)
        grid.addWidget(button, 8, 2)

        button = QPushButton("<")
        button.clicked.connect(self.reduce)
        grid.addWidget(button, 8, 3)

        self.engineer(False)
        self.setGeometry(50, 50, 600, 200)
        self.setWindowTitle("PyQt Example")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("design.qss").read_text())
    window = MyWindow()
    sys.exit(app.exec_())

# TODO  корректность ввода тригонометрии
