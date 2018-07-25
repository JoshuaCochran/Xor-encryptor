import sys, datetime
from os import urandom, chdir, getcwd, sep, pardir, path
from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QGridLayout, QApplication, QLineEdit, QFileDialog, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, QDir


class EncryptionFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.key = 0xA8
        self.randomKey = False

        self.resize(400, 200)
        self.setWindowTitle('Xor Encryptor')

        inputLabel = QLabel('Input path: ')
        self.inputEdit = QLineEdit()

        outputLabel = QLabel('Output path: ')
        self.outputEdit = QLineEdit()

        keyLabel = QLabel("Key: ")
        self.keyEdit = QLineEdit()
        self.keyEdit.setPlaceholderText("Generate randomly or select key file")
        self.keyEdit.setReadOnly(True)
        self.keyRandomButton = QPushButton("Generate Key")
        self.keyRandomButton.clicked.connect(self.on_random_click)
        self.keyFileNavButton = QPushButton("Select Key")
        self.keyFileNavButton.clicked.connect(self.on_file_nav_click)

        self.executeButton = QPushButton("Execute")
        self.executeButton.clicked.connect(self.on_button_click)

        grid = QGridLayout()
        grid.setSpacing(10)

        subLayout1 = QHBoxLayout()
        subLayout1.addWidget(inputLabel)
        subLayout1.addWidget(self.inputEdit)

        subLayout2 = QHBoxLayout()
        subLayout2.addWidget(outputLabel)
        subLayout2.addWidget(self.outputEdit)

        subLayout3 = QHBoxLayout()
        subLayout3.addWidget(keyLabel)
        subLayout3.addWidget(self.keyEdit)

        subLayout4 = QHBoxLayout()
        subLayout4.addWidget(self.keyRandomButton)
        subLayout4.addWidget(self.keyFileNavButton)

        grid.addLayout(subLayout1, 0, 0)
        grid.addLayout(subLayout2, 1, 0)
        grid.addLayout(subLayout3, 2, 0)
        grid.addLayout(subLayout4, 3, 0)
        grid.addWidget(self.executeButton, 4, 0)

        self.setLayout(grid)
        self.show()

    def genkey(self, length):
        return urandom(length)

    def xordata(self, a, key1):
        return bytearray([b ^ keyInstance for b, keyInstance in zip(bytearray(a), key1)])

    def encrypt(self):
        with open(self.inputEdit.text(), 'rb') as inf:
            data = inf.read()
            if self.randomKey:
                self.key = self.genkey(len(data))

            data2 = self.xordata(data, self.key)

        with open(self.outputEdit.text(), 'wb') as outf:
            outf.write(data2)

        folder = getcwd()
        date = datetime.datetime.now().strftime("%Y-%m-%d %Hhr%Mmin%Ss")
        with open(folder + "/" + date + ".key", 'wb') as outf:
            outf.write(self.key)

    @pyqtSlot()
    def on_button_click(self):
        self.encrypt()

    @pyqtSlot()
    def on_file_nav_click(self):
        file, _filter = QFileDialog.getOpenFileName(self, "Select Key", QDir.currentPath())

        with open(file, 'rb') as inf:
            self.key = inf.read()

        self.keyEdit.setPlaceholderText(file)

    @pyqtSlot()
    def on_random_click(self):
        self.randomKey = True
        self.keyEdit.setPlaceholderText("Random key")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    frame = EncryptionFrame()
    sys.exit(app.exec_())
