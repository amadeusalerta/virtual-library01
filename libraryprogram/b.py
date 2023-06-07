import sys
import re
import mysql.connector
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QDialog, QComboBox, QInputDialog
from PyQt5.QtGui import QPixmap

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Paneli")
        self.resize(300, 200)

        layout = QVBoxLayout()

        label_eposta = QLabel("E-posta:")
        self.lineedit_eposta = QLineEdit()
        layout.addWidget(label_eposta)
        layout.addWidget(self.lineedit_eposta)

        label_password = QLabel("Şifre:")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password)
        layout.addWidget(self.lineedit_password)

        button_login = QPushButton("Giriş Yap")
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login)

        button_register = QPushButton("Yeni Hesap Oluştur")
        button_register.clicked.connect(self.openRegisterWindow)
        layout.addWidget(button_register)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def login(self):
        eposta = self.lineedit_eposta.text()
        password = self.lineedit_password.text()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM kullanici WHERE eposta = %s AND sifre = %s"
        params = (eposta, password)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            role = result[3]
            if role == "ogrenci":
                self.student_window = StudentWindow(eposta)
                self.student_window.show()
            elif role == "ogretmen":
                self.teacher_window = TeacherWindow(eposta)
                self.teacher_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz e-posta veya şifre!")

        cursor.close()
        connection.close()

    def openRegisterWindow(self):
        self.register_window = RegisterWindow()
        self.register_window.register_success.connect(self.registerSuccess)
        self.register_window.show()

    def registerSuccess(self):
        QMessageBox.information(self, "Başarılı", "Başarıyla kayıt oldunuz!")

class RegisterWindow(QDialog):
    register_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.resize(300, 200)

        layout = QVBoxLayout()

        label_eposta = QLabel("E-posta:")
        self.lineedit_eposta = QLineEdit()
        layout.addWidget(label_eposta)
        layout.addWidget(self.lineedit_eposta)

        label_password = QLabel("Şifre:")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password)
        layout.addWidget(self.lineedit_password)

        label_role = QLabel("Rol:")
        self.combobox_role = QComboBox()
        self.combobox_role.addItem("ogrenci")
        self.combobox_role.addItem("ogretmen")
        layout.addWidget(label_role)
        layout.addWidget(self.combobox_role)

        button_register = QPushButton("Kayıt Ol")
        button_register.clicked.connect(self.register)
        layout.addWidget(button_register)

        self.setLayout(layout)

    def register(self):
        eposta = self.lineedit_eposta.text()
        password = self.lineedit_password.text()
        role = self.combobox_role.currentText()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "INSERT INTO kullanici (eposta, sifre, rol) VALUES (%s, %s, %s)"
        params = (eposta, password, role)
        cursor.execute(query, params)
        connection.commit()

        cursor.close()
        connection.close()

        self.register_success.emit()
        self.close()

class StudentWindow(QMainWindow):
    def __init__(self, eposta):
        super().__init__()
        self.setWindowTitle("Öğrenci Paneli")
        self.resize(300, 200)

        layout = QVBoxLayout()

        label_welcome = QLabel(f"Hoş geldiniz, {eposta}!")
        layout.addWidget(label_welcome)

        button_logout = QPushButton("Çıkış Yap")
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class TeacherWindow(QMainWindow):
    def __init__(self, eposta):
        super().__init__()
        self.setWindowTitle("Öğretmen Paneli")
        self.resize(300, 200)

        layout = QVBoxLayout()

        label_welcome = QLabel(f"Hoş geldiniz, {eposta}!")
        layout.addWidget(label_welcome)

        button_logout = QPushButton("Çıkış Yap")
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
