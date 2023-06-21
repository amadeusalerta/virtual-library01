from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector as mc
from PyQt5.QtWidgets import QDialog


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 193)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditEmail = QtWidgets.QLineEdit(Form)
        self.lineEditEmail.setObjectName("lineEditEmail")
        self.horizontalLayout.addWidget(self.lineEditEmail)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEditPassword = QtWidgets.QLineEdit(Form)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.horizontalLayout_2.addWidget(self.lineEditPassword)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
       QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")

        #this is the signal that we have already connected
        self.pushButton.clicked.connect(self.login)
        self.verticalLayout.addWidget(self.pushButton)
        self.labelResult = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelResult.setFont(font)
        self.labelResult.setText("")
        self.labelResult.setObjectName("labelResult")
        self.verticalLayout.addWidget(self.labelResult)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def login(self):
        try:
            email = self.lineEditEmail.text()
            password = self.lineEditPassword.text()

            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Efehan33!",
                database="libraryprogram"


            )

            mycursor = mydb.cursor()
            query = "SELECT email,password from users where email " \
                    "like '"+email + "'and password like '" \
                    + password + "'"
            mycursor.execute(query)
            result = mycursor.fetchone()

            if result == None:
                self.labelResult.setText("Incorrect email or password")

            else:
                self.labelResult.setText("You are logged in")
                


        except mc.Error as e:
            self.labelResult.setText("Error")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Email:"))
        self.label_2.setText(_translate("Form", "Password:"))
        self.pushButton.setText(_translate("Form", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())