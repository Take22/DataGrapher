import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/ErrorDialog.ui")[0]

class ErrorDialog(QDialog, form_class):
    def __init__(self, errorText):
        super().__init__()
        self.setupUi(self)

        self.errorText = errorText
        self.errorContents.setText(self.errorText)

        self.okButton.clicked.connect(self.pushOkButtonClicked)

    def pushOkButtonClicked(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ErrorDialog()
    main.show()
    sys.exit(app.exec_())

    
