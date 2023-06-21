import sys
import re
import mysql.connector
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
            if role == "Öğrenci":
                self.student_window = StudentWindow(eposta)
                self.student_window.show()
            elif role == "Öğretmen":
                self.teacher_window = TeacherWindow(eposta)
                self.teacher_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz e-posta veya şifre!")

        cursor.close()
        connection.close()

    def openRegisterWindow(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

class RegisterWindow(QDialog):
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
        self.combobox_role.addItem("Öğrenci")
        self.combobox_role.addItem("Öğretmen")
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

        QMessageBox.information(self, "Başarılı", "Hesap başarıyla oluşturuldu.")

        cursor.close()
        connection.close()
        self.close()

class StudentWindow(QMainWindow):
    def __init__(self, eposta):
        super().__init__()
        self.setWindowTitle("Öğrenci Kütüphane")
        self.resize(400, 300)

        self.eposta = eposta

        layout = QVBoxLayout()

        self.listwidget_books = QListWidget()
        layout.addWidget(self.listwidget_books)

        button_borrow = QPushButton("Kitap Kirala")
        button_borrow.clicked.connect(self.borrowBook)
        layout.addWidget(button_borrow)

        button_add_book = QPushButton("Kitap Ekle")
        button_add_book.clicked.connect(self.openAddBookWindow)
        layout.addWidget(button_add_book)

        button_account = QPushButton("Hesabımı Görüntüle")
        button_account.clicked.connect(self.openAccountWindow)
        layout.addWidget(button_account)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.loadBooks()

    def loadBooks(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM kitaplar"
        cursor.execute(query)
        result = cursor.fetchall()

        for book in result:
            item = QListWidgetItem(book[1])
            self.listwidget_books.addItem(item)

        cursor.close()
        connection.close()

    def borrowBook(self):
        selected_item = self.listwidget_books.currentItem()
        if selected_item:
            book_title = selected_item.text()
            QMessageBox.information(self, "Kitap Kiralama", f"{book_title} kitabını kiraladınız.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir kitap seçin.")

    def openAddBookWindow(self):
        self.add_book_window = AddBookWindow()
        self.add_book_window.show()

    def openAccountWindow(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM kullanici WHERE eposta = %s"
        params = (self.eposta,)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            self.account_window = AccountWindow(result)
            self.account_window.show()

        cursor.close()
        connection.close()

class TeacherWindow(QMainWindow):
    def __init__(self, eposta):
        super().__init__()
        self.setWindowTitle("Öğretmen Kütüphane")
        self.resize(400, 300)

        self.eposta = eposta

        layout = QVBoxLayout()

        self.listwidget_books = QListWidget()
        layout.addWidget(self.listwidget_books)

        button_add_book = QPushButton("Kitap Ekle")
        button_add_book.clicked.connect(self.openAddBookWindow)
        layout.addWidget(button_add_book)

        button_account = QPushButton("Hesabımı Görüntüle")
        button_account.clicked.connect(self.openAccountWindow)
        layout.addWidget(button_account)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.loadBooks()

    def loadBooks(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM kitaplar"
        cursor.execute(query)
        result = cursor.fetchall()

        for book in result:
            item = QListWidgetItem(book[1])
            self.listwidget_books.addItem(item)

        cursor.close()
        connection.close()

    def openAddBookWindow(self):
        self.add_book_window = AddBookWindow()
        self.add_book_window.show()

    def openAccountWindow(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM kullanici WHERE eposta = %s"
        params = (self.eposta,)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            self.account_window = AccountWindow(result)
            self.account_window.show()

        cursor.close()
        connection.close()

class AddBookWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Ekle")
        self.resize(300, 200)

        layout = QVBoxLayout()

        label_title = QLabel("Kitap Adı:")
        self.lineedit_title = QLineEdit()
        layout.addWidget(label_title)
        layout.addWidget(self.lineedit_title)

        button_add = QPushButton("Ekle")
        button_add.clicked.connect(self.addBook)
        layout.addWidget(button_add)

        self.setLayout(layout)

    def addBook(self):
        title = self.lineedit_title.text()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "INSERT INTO kitaplar (kitap_adi) VALUES (%s)"
        params = (title,)
        cursor.execute(query, params)
        connection.commit()

        QMessageBox.information(self, "Başarılı", "Kitap başarıyla eklendi.")

        cursor.close()
        connection.close()
        self.close()

class AccountWindow(QDialog):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Hesap Bilgileri")
        self.resize(300, 200)

        layout = QVBoxLayout()

        label_eposta = QLabel(f"E-posta: {user[1]}")
        layout.addWidget(label_eposta)

        label_password = QLabel("Şifre:")
        self.lineedit_password = QLineEdit(user[2])
        layout.addWidget(label_password)
        layout.addWidget(self.lineedit_password)

        button_save = QPushButton("Kaydet")
        button_save.clicked.connect(self.savePassword)
        layout.addWidget(button_save)

        self.setLayout(layout)

    def savePassword(self):
        password = self.lineedit_password.text()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "UPDATE kullanici SET sifre = %s WHERE eposta = %s"
        params = (password, self.eposta)
        cursor.execute(query, params)
        connection.commit()

        QMessageBox.information(self, "Başarılı", "Şifre başarıyla güncellendi.")

        cursor.close()
        connection.close()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
