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
        self.resize(500, 400)

        self.eposta = eposta

        layout = QVBoxLayout()

        label_welcome = QLabel(f"Hoş geldiniz, {self.eposta}!")
        layout.addWidget(label_welcome)

        button_borrow = QPushButton("Kitap Ödünç Al")
        button_borrow.clicked.connect(self.borrowBook)
        layout.addWidget(button_borrow)

        button_return = QPushButton("Kitap İade Et")
        button_return.clicked.connect(self.returnBook)
        layout.addWidget(button_return)

        button_logout = QPushButton("Çıkış Yap")
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def borrowBook(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT * FROM kitaplar WHERE durum = 'kiralanmadi'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            book_names = [book[1] for book in result]
            book_name, ok = QInputDialog.getItem(self, "Kitap Seç", "Ödünç almak istediğiniz kitabı seçin:", book_names, editable=False)
            if ok and book_name:
                book_id = None
                for book in result:
                    if book[1] == book_name:
                        book_id = book[0]
                        break

                query = "INSERT INTO kiralama (kullanici_id, kitap_id, kiralama_tarihi, iade_tarihi) VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY))"
                params = (self.getUserID(), book_id)
                cursor.execute(query, params)

                query = "UPDATE kitaplar SET durum = 'kiralandi' WHERE id = %s"
                cursor.execute(query, (book_id,))

                connection.commit()

                QMessageBox.information(self, "Başarılı", "Kitap ödünç alındı!")
            else:
                QMessageBox.warning(self, "Hata", "Kitap seçilmedi!")
        else:
            QMessageBox.warning(self, "Hata", "Ödünç alınacak kitap bulunamadı!")

        cursor.close()
        connection.close()

    def returnBook(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT kitaplar.ad, kiralama.id FROM kitaplar INNER JOIN kiralama ON kitaplar.id = kiralama.kitap_id WHERE kitaplar.durum = 'kiralandi' AND kiralama.kullanici_id = %s"
        params = (self.getUserID(),)
        cursor.execute(query, params)
        result = cursor.fetchall()

        if result:
            book_ids = [book[1] for book in result]
            book_name, ok = QInputDialog.getItem(self, "Kitap Seç", "İade etmek istediğiniz kitabı seçin:", [book[0] for book in result], editable=False)
            if ok and book_name:
                book_id = None
                for book in result:
                    if book[0] == book_name:
                        book_id = book[1]
                        break

                query = "DELETE FROM kiralama WHERE id = %s"
                cursor.execute(query, (book_id,))

                query = "UPDATE kitaplar SET durum = 'kiralanmadi' WHERE id = %s"
                cursor.execute(query, (book_id,))

                connection.commit()

                QMessageBox.information(self, "Başarılı", "Kitap iade edildi!")
            else:
                QMessageBox.warning(self, "Hata", "Kitap seçilmedi!")
        else:
            QMessageBox.warning(self, "Hata", "İade edilecek kitap bulunamadı!")

        cursor.close()
        connection.close()

    def getUserID(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "SELECT id FROM kullanici WHERE eposta = %s"
        cursor.execute(query, (self.eposta,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result[0]

    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class TeacherWindow(QMainWindow):
    def __init__(self, eposta):
        super().__init__()
        self.setWindowTitle("Öğretmen Paneli")
        self.resize(500, 400)


        

        self.eposta = eposta

        layout = QVBoxLayout()

        label_welcome = QLabel(f"Hoş geldiniz, {self.eposta}!")
        layout.addWidget(label_welcome)

        button_add_book = QPushButton("Kitap Ekle")
        button_add_book.clicked.connect(self.addBook)
        layout.addWidget(button_add_book)

        button_remove_book = QPushButton("Kitap Sil")
        button_remove_book.clicked.connect(self.removeBook)
        layout.addWidget(button_remove_book)

        button_logout = QPushButton("Çıkış Yap")
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.book_list = QListWidget()
        layout.addWidget(self.book_list)


    def addBook(self):
        self.add_book_dialog = AddBookDialog()
        self.add_book_dialog.book_added.connect(self.refreshBookList)
        self.add_book_dialog.show()

    def removeBook(self):
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

        if result:
            book_names = [book[1] for book in result]
            book_name, ok = QInputDialog.getItem(self, "Kitap Seç", "Silmek istediğiniz kitabı seçin:", book_names, editable=False)
            if ok and book_name:
                book_id = None
                for book in result:
                    if book[1] == book_name:
                        book_id = book[0]
                        break

                query = "DELETE FROM kitaplar WHERE id = %s"
                cursor.execute(query, (book_id,))

                connection.commit()

                QMessageBox.information(self, "Başarılı", "Kitap silindi!")
                self.refreshBookList()
            else:
                QMessageBox.warning(self, "Hata", "Kitap seçilmedi!")
        else:
            QMessageBox.warning(self, "Hata", "Silinecek kitap bulunamadı!")

        cursor.close()
        connection.close()

    def refreshBookList(self):
        self.book_list.clear()

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
            item = QListWidgetItem(f"{book[1]} - {book[2]} - {book[3]}")
            self.book_list.addItem(item)

        cursor.close()
        connection.close()

    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class AddBookDialog(QDialog):
    book_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Ekle")
        self.resize(300, 200)

        layout = QVBoxLayout()

        label_title = QLabel("Kitap Adı:")
        self.lineedit_title = QLineEdit()
        layout.addWidget(label_title)
        layout.addWidget(self.lineedit_title)

        label_author = QLabel("Yazar:")
        self.lineedit_author = QLineEdit()
        layout.addWidget(label_author)
        layout.addWidget(self.lineedit_author)

        label_publish_date = QLabel("Yayın Tarihi:")
        self.lineedit_publish_date = QLineEdit()
        layout.addWidget(label_publish_date)
        layout.addWidget(self.lineedit_publish_date)

        label_category = QLabel("Kategori:")
        self.lineedit_category = QLineEdit()
        layout.addWidget(label_category)
        layout.addWidget(self.lineedit_category)

        button_add = QPushButton("Ekle")
        button_add.clicked.connect(self.addBook)
        layout.addWidget(button_add)

        self.setLayout(layout)

    def addBook(self):
        title = self.lineedit_title.text()
        author = self.lineedit_author.text()
        publish_date = self.lineedit_publish_date.text()
        category = self.lineedit_category.text()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "INSERT INTO kitaplar (ad, yazar, yayin_tarihi, kategori) VALUES (%s, %s, %s, %s)"
        params = (title, author, publish_date, category)
        cursor.execute(query, params)
        connection.commit()

        cursor.close()
        connection.close()

        self.book_added.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
