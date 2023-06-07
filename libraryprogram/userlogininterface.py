import typing
from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.QtWidgets import QWidget
from logscreen import Ui_LogInterface
import mysql.connector as mc

class Application01(QtWidgets.QMainWindow):
    def __init__(self):
        super(Application01,self).__init__()
        self.ui =Ui_LogInterface()
        self.ui.setupUi(self) 
def app():
   app=QtWidgets.QApplication(sys.argv)
   win=Application01()
   win.show()
   sys.exit(app.exec_())

app()