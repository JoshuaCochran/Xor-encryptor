import sys
from os import urandom
from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QGridLayout, QApplication, QLineEdit
from PyQt5.QtCore import pyqtSlot


class EncryptionFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.resize(400, 200)
        self.setWindowTitle('Xor Encryptor')

        inputLabel = QLabel('Input path: ')
        self.inputEdit = QLineEdit()

        outputLabel = QLabel('Output path: ')
        self.outputEdit = QLineEdit()

        keyLabel = QLabel("Key: ")
        self.keyEdit = QLineEdit()
        self.keyEdit.setPlaceholderText("blank for default")

        self.executeButton = QPushButton("Execute")
        self.executeButton.clicked.connect(self.on_button_click)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(inputLabel, 0, 0)
        grid.addWidget(outputLabel, 1, 0)
        grid.addWidget(self.inputEdit, 0, 1)
        grid.addWidget(self.outputEdit, 1, 1)
        grid.addWidget(keyLabel, 2, 0)
        grid.addWidget(self.keyEdit, 2, 1)
        grid.addWidget(self.executeButton, 3, 1)

        self.setLayout(grid)
        self.show()

    def genkey(self, length):
        return urandom(length)

    def xordata(self, a, key1):
        return bytearray([b ^ keyInstance for b, keyInstance in zip(bytearray(a), key1)])

    @pyqtSlot()
    def on_button_click(self):
        with open(self.inputEdit.text(), 'rb') as inf:
            data = inf.read()
            key = self.genkey(len(data))
            data2 = self.xordata(data, key)

        with open(self.outputEdit.text(), 'wb') as outf:
            outf.write(data2)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    frame = EncryptionFrame()
    sys.exit(app.exec_())
