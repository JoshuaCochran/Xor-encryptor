import sys, datetime
from os import urandom, chdir, getcwd, sep, pardir, path
from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QGridLayout, QApplication, QLineEdit, QFileDialog, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, QDir


class EncryptionFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.key = 0x00
        self.randomKey = False

        self.resize(400, 200)
        self.setWindowTitle('Xor Encryptor')

        inputLabel = QLabel('Input path: ')
        self.inputEdit = QLineEdit()
        self.inputEdit.setReadOnly(True)
        self.inputEdit.setPlaceholderText("Select file")
        self.inputButton = QPushButton("Select File")
        self.inputButton.clicked.connect(self.on_input_click)

        outputLabel = QLabel('Output path: ')
        self.outputEdit = QLineEdit()
        self.outputEdit.setReadOnly(True)
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

    def xordata(self, a, key1):
        return bytearray([b ^ keyInstance for b, keyInstance in zip(bytearray(a), key1)])

    def encrypt(self):
        if not self.randomKey and self.key == 0x00:
            return

        if self.inputEdit.text() != "" and self.inputEdit.text != "Path not found":
            with open(self.inputEdit.text(), 'rb') as inf:
                data = inf.read()
                if self.randomKey:
                    self.key = self.genkey(len(data))
        else:
            return

        data2 = self.xordata(data, self.key)
        if self.outputEdit.text() != "" and self.outputEdit.text != "Path not found":
            with open(self.outputEdit.text(), 'wb') as outf:
                outf.write(data2)
        else:
            return

        folder = getcwd()
        date = datetime.datetime.now().strftime("%Y-%m-%d %Hhr%Mmin%Ss")
        with open(folder + "/" + date + ".txt", 'wb') as outf:
            outf.write(self.key)

    @pyqtSlot()
    def on_button_click(self):
        self.encrypt()

    @pyqtSlot()
    def on_key_select_click(self):
        file, _filter = QFileDialog.getOpenFileName(self, "Select Key", QDir.currentPath())

        if file != "":
            with open(file, 'rb') as inf:
                self.key = inf.read()

        self.keyEdit.setPlaceholderText(file)

    @pyqtSlot()
    def on_random_click(self):
        self.randomKey = True
        self.keyEdit.setPlaceholderText("Random key")

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
