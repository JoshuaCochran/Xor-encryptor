import sys
import datetime
from os import urandom, getcwd
from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QGridLayout, QApplication, QLineEdit, QFileDialog, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, QDir


class EncryptionFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.key = bytearray(0x00)
        self.randomKey = False

        self.resize(400, 200)
        self.setWindowTitle('Xor Encryptor')

        inputLabel = QLabel('Input path: ')
        self.inputEdit = QLineEdit()
        self.inputEdit.setPlaceholderText("Select file")
        self.inputButton = QPushButton("Select File")
        self.inputButton.clicked.connect(self.on_input_click)

        outputLabel = QLabel('Output path: ')
        self.outputEdit = QLineEdit()
        self.outputEdit.setPlaceholderText("Select file")
        self.outputButton = QPushButton("Select File")
        self.outputButton.clicked.connect(self.on_output_click)

        keyLabel = QLabel("Key: ")
        self.keyEdit = QLineEdit()
        self.keyEdit.setPlaceholderText("Generate randomly or select key file")
        self.keyEdit.setReadOnly(True)
        self.keyRandomButton = QPushButton("Generate Key")
        self.keyRandomButton.clicked.connect(self.on_random_click)
        self.keyFileNavButton = QPushButton("Select Key")
        self.keyFileNavButton.clicked.connect(self.on_key_select_click)

        self.executeButton = QPushButton("Execute")
        self.executeButton.clicked.connect(self.on_button_click)

        grid = QGridLayout()
        grid.setSpacing(10)

        subLayout1 = QHBoxLayout()
        subLayout1.addWidget(inputLabel)
        subLayout1.addWidget(self.inputEdit)
        subLayout1.addWidget(self.inputButton)

        subLayout2 = QHBoxLayout()
        subLayout2.addWidget(outputLabel)
        subLayout2.addWidget(self.outputEdit)
        subLayout2.addWidget(self.outputButton)

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

    def xordata(self, data, key):
        if len(data) < len(key):
            raise ValueError("Invalid key length. Key length must be greater than or equal to data size.")
        try:
            return bytearray([dataByte ^ keyByte for dataByte, keyByte in zip(bytearray(data), key)])
        except TypeError:
            print("Error! Invalid data or key. Try again...")

    def encryptionHandler(self):
        if not self.randomKey and self.key == bytearray(0x00):
            return

        try:
            inf = open(self.inputEdit.text(), 'rb')
        except IOError:
            print("Could not read file:", self.inputEdit.text())
            return
        else:
            with inf:
                data = inf.read()

        if self.randomKey:
            self.key = self.genkey(len(data))

        encryptedData = self.xordata(data, self.key)

        try:
            outf = open(self.outputEdit.text(), 'wb')
        except IOError:
            print("Could not read file:", self.outputEdit.text())
            return
        else:
            with outf:
                outf.write(encryptedData)

        folder = getcwd()
        date = datetime.datetime.now().strftime("%Y-%m-%d %Hhr%Mmin%Ss")
        with open(folder + "/" + date + ".txt", 'wb') as outf:
            outf.write(self.key)

        self.key = bytearray(0x00)

    @pyqtSlot()
    def on_button_click(self):
        self.encryptionHandler()

    @pyqtSlot()
    def on_key_select_click(self):
        self.randomKey = False
        file, _filter = QFileDialog.getOpenFileName(self, "Select Key", QDir.currentPath())

        try:
            inf = open(file, 'rb')
        except IOError:
            print("file not found:", file)
        else:
            with inf:
                self.key = inf.read()

        self.keyEdit.setText(file)

    @pyqtSlot()
    def on_random_click(self):
        self.randomKey = True
        self.keyEdit.setText("Random key")

    @pyqtSlot()
    def on_input_click(self):
        file, _filter = QFileDialog.getOpenFileName(self, "Select Input FIle", QDir.currentPath())
        if file != "":
            self.inputEdit.setText(file)
        else:
            self.inputEdit.setText("Path not found")

    @pyqtSlot()
    def on_output_click(self):
        file, _filter = QFileDialog.getOpenFileName(self, "Select Input FIle", QDir.currentPath())
        if file != "":
            self.outputEdit.setText(file)
        else:
            self.outputEdit.setText("Path not found")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    frame = EncryptionFrame()
    sys.exit(app.exec_())
