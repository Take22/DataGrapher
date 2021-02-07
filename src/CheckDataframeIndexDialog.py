import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/CheckDataframeIndexDialog.ui")[0]


class CheckDataframeIndexDialog(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.dataframeIndex = 0

        self.okButton.clicked.connect(self.pushOkButtonClicked)

    def pushOkButtonClicked(self):
        if self.includedButton.isChecked():
            self.dataframeIndex = 0
        elif self.notIncludedButton.isChecked():
            self.dataframeIndex = 1
        else:
            print("unexpected error")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CheckDataframeIndexDialog()
    main.show()
    sys.exit(app.exec_())
