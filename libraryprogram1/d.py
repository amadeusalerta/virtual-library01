import sys
import re
import hashlib
import mysql.connector
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QListWidgetItem, QDialog, QComboBox, QInputDialog,QDialogButtonBox
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

        admin_login_button = QPushButton("Yönetici Girişi")
        admin_login_button.clicked.connect(self.admin_login)
        layout.addWidget(admin_login_button)


        button_register = QPushButton("Yeni Hesap Oluştur")
        button_register.clicked.connect(self.openRegisterWindow)
        layout.addWidget(button_register)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def admin_login(self):
     email = self.lineedit_eposta.text()
     password = self.lineedit_password.text()
    
     if email == "sussybaka33@gmail.com" and password == "amogusdrip01":
        self.successful_login()
     else:
        self.failed_login()

        
    def successful_login(self):
        QMessageBox.information(self, "Başarılı Giriş", "Başarıyla giriş yapıldı.")
        self.admin_window = AdminWindow()
        
    def failed_login(self):
        QMessageBox.warning(self, "Hatalı Giriş", "Eposta veya şifre hatalı.")


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

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Paneli")
        self.resize(1280, 720)

        # MySQL bağlantı bilgileri
        # host = "localhost"
        # user = "root"
        # password = "Efehan33!"
        # database = "libraryprogram"

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        # Kullanıcılar için QTableWidget
        self.user_table = QTableWidget(self)
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["E-Posta", "Şifre", "Rol"])

        # Kitaplar için QTableWidget
        self.book_table = QTableWidget(self)
        self.book_table.setColumnCount(5)
        self.book_table.setHorizontalHeaderLabels(
            ["Ad", "Yazar", "Yayın Tarihi", "Kategori", "Durum"]
        )

        # Verileri yükle
        self.load_users(cursor)
        self.load_books(cursor)

        # Butonlar
        button_user_add = QPushButton("Kullanıcı Ekle")
        button_user_add.clicked.connect(self.add_user)
        button_user_remove = QPushButton("Kullanıcı Sil")
        button_user_remove.clicked.connect(self.remove_user)
        button_book_add = QPushButton("Kitap Ekle")
        button_book_add.clicked.connect(self.add_book)
        button_book_remove = QPushButton("Kitap Sil")
        button_book_remove.clicked.connect(self.remove_book)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(button_user_add)
        layout.addWidget(button_user_remove)
        layout.addWidget(self.user_table)
        layout.addWidget(button_book_add)
        layout.addWidget(button_book_remove)
        layout.addWidget(self.book_table)

        # Widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def load_users(self, cursor):
        # Kullanıcıları veritabanından al
        cursor.execute("SELECT eposta, sifre, rol FROM kullanici")
        users = cursor.fetchall()

        # Kullanıcıları QTableWidget'e ekle
        self.user_table.setRowCount(len(users))
        for row, user in enumerate(users):
            for col, data in enumerate(user):
                item = QTableWidgetItem(str(data))
                self.user_table.setItem(row, col, item)

    def load_books(self, cursor):
        # Kitapları veritabanından al
        cursor.execute("SELECT ad, yazar, yayin_tarihi, kategori, durum FROM kitaplar")
        books = cursor.fetchall()

        # Kitapları QTableWidget'e ekle
        self.book_table.setRowCount(len(books))
        for row, book in enumerate(books):
            for col, data in enumerate(book):
                item = QTableWidgetItem(str(data))
                self.book_table.setItem(row, col, item)
        
        self.show()

    def add_user(self):
        dialog01 = AddUserDialog()
        if dialog01.exec_() == QDialog.Accepted:
            email = dialog01.email_line.text()
            password = dialog01.password_line.text()
            role = dialog01.role_combo.currentText()

            # Kullanıcıyı veritabanına ekle
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Efehan33!",
                database="libraryprogram"
            )
            cursor = connection.cursor()
            query = "INSERT INTO kullanici (eposta, sifre, rol) VALUES (%s, %s, %s)"
            values = (email, password, role)
            cursor.execute(query, values)
            connection.commit()

            # Kullanıcıları güncelle
            self.load_users(cursor)

            # İşlem tamamlandı mesajı göster
            QMessageBox.information(self, "Başarılı", "Kullanıcı başarıyla eklendi.")

    def remove_user(self):
        selected_rows = self.user_table.selectionModel().selectedRows()
        if len(selected_rows) > 0:
            # Seçili kullanıcıları sil
            emails = []
            for row in selected_rows:
                email = self.user_table.item(row.row(), 0).text()
                emails.append(email)

            # Veritabanından sil
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Efehan33!",
                database="libraryprogram"
            )
            cursor = connection.cursor()
            query = "DELETE FROM kullanici WHERE eposta IN (%s)"
            values = tuple(emails)
            cursor.execute(query, values)
            connection.commit()

            # Kullanıcıları güncelle
            self.load_users(cursor)

            # İşlem tamamlandı mesajı göster
            QMessageBox.information(self, "Başarılı", "Seçili kullanıcılar başarıyla silindi.")

    def add_book(self):
        dialog = AddBookDialog()
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_line.text()
            author = dialog.author_line.text()
            date = dialog.date_line.text()
            category = dialog.category_combo.currentText()
            status = dialog.status_combo.currentText()

            # Kitabı veritabanına ekle
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Efehan33!",
                database="libraryprogram"
            )
            cursor = connection.cursor()
            query = "INSERT INTO kitaplar (ad, yazar, yayin_tarihi, kategori, durum) VALUES (%s, %s, %s, %s, %s)"
            values = (name, author, date, category, status)
            cursor.execute(query, values)
            connection.commit()

            # Kitapları güncelle
            self.load_books(cursor)

            # İşlem tamamlandı mesajı göster
            QMessageBox.information(self, "Başarılı", "Kitap başarıyla eklendi.")

    def removeBook(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "DELETE FROM kitaplar WHERE id = %s"
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

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kullanıcı Ekle")

        self.email_label = QLabel("E-posta:")
        self.email_line = QLineEdit()

        self.password_label = QLabel("Şifre:")
        self.password_line = QLineEdit()
        self.password_line.setEchoMode(QLineEdit.Password)

        self.role_label = QLabel("Rol:")
        self.role_combo = QComboBox()
        self.role_combo.addItem("Admin")
        self.role_combo.addItem("Kullanıcı")

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_line)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_line)
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_combo)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


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
    
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if not eposta.endswith("@gmail.com"):
         QMessageBox.warning(self, "Hata", "Geçersiz e-posta adresi! E-posta adresi @gmail.com ile bitmelidir.")
         return

        query = "INSERT INTO kullanici (eposta, sifre, rol) VALUES (%s, %s, %s)"
        params = (eposta, password, role)
        cursor.execute(query, params)
        connection.commit()

        query = "INSERT INTO hashli_kodlar (k_id, hashli_sifre) VALUES (%s, %s)"
        params = (eposta, hashed_password)
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
        self.resize(600, 400)

        self.eposta = eposta

        layout = QVBoxLayout()

        label_welcome = QLabel(f"Hoş geldiniz, {self.eposta}!")
        layout.addWidget(label_welcome)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Kitap Adı", "Yazar", "Yayın Tarihi", "Kategori"])
        layout.addWidget(self.table_widget)

        button_borrow = QPushButton("Kitap Ödünç Al")
        button_borrow.clicked.connect(self.borrowBook)
        layout.addWidget(button_borrow)

        button_return = QPushButton("Kitap İade Et")
        button_return.clicked.connect(self.returnBook)
        layout.addWidget(button_return)

        button_logout = QPushButton("Çıkış Yap")
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        button_search = QPushButton("Kitap Ara")
        button_search.clicked.connect(self.searchBook)
        layout.addWidget(button_search)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.refreshBookList()

    def refreshBookList(self):
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

        self.table_widget.setRowCount(len(result))

        for row, book in enumerate(result):
            for col, data in enumerate(book[1:]):
                item = QTableWidgetItem(str(data))
                self.table_widget.setItem(row, col, item)

        cursor.close()
        connection.close()

    def searchBook(self):
      keyword, ok = QInputDialog.getText(self, "Kitap Ara", "Aramak istediğiniz kitap adını girin:")
      if ok and keyword:
          connection = mysql.connector.connect(
              host="localhost",
              user="root",
              password="Efehan33!",
              database="libraryprogram"
          )
          cursor = connection.cursor()

          query = "SELECT ad, yazar, yayin_tarihi, kategori FROM kitaplar WHERE ad LIKE %s"
          params = ('%' + keyword + '%',)
          cursor.execute(query, params)
          result = cursor.fetchall()

          self.table_widget.setRowCount(len(result))
          for row, book in enumerate(result):
              for col, data in enumerate(book):
                  item = QTableWidgetItem(str(data))
                  self.table_widget.setItem(row, col, item)

          cursor.close()
          connection.close()


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
            book_name, ok = QInputDialog.getItem(self, "Kitap Seç", "Ödünç almak istediğiniz kitab seçin:", book_names, editable=False)
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

     query = "SELECT * FROM kitaplar WHERE durum = 'kiralandi'"
     cursor.execute(query)
     result = cursor.fetchall()

     if result:
         book_names = [book[1] for book in result]
         book_name, ok = QInputDialog.getItem(self, "Kitap Seç", "İade etmek istediğiniz kitabı seçin:", book_names, editable=False)
         if ok and book_name:
             book_id = None
             for book in result:
                 if book[1] == book_name:
                     book_id = book[0]
                     break

             query = "DELETE FROM kiralama WHERE kitap_id = %s"
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

        button_search = QPushButton("Kitap Ara")
        button_search.clicked.connect(self.searchBook)
        layout.addWidget(button_search)

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
    
    def searchBook(self):
      keyword, ok = QInputDialog.getText(self, "Kitap Ara", "Aramak istediğiniz kitap adını girin:")
      if ok and keyword:
          connection = mysql.connector.connect(
              host="localhost",
              user="root",
              password="Efehan33!",
              database="libraryprogram"
          )
          cursor = connection.cursor()

          query = "SELECT ad, yazar, yayin_tarihi, kategori FROM kitaplar WHERE ad LIKE %s"
          params = ('%' + keyword + '%',)
          cursor.execute(query, params)
          result = cursor.fetchall()

          self.table_widget.setRowCount(len(result))
          for row, book in enumerate(result):
              for col, data in enumerate(book):
                  item = QTableWidgetItem(str(data))
                  self.table_widget.setItem(row, col, item)

          cursor.close()
          connection.close()

    def removeBook(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Efehan33!",
            database="libraryprogram"
        )
        cursor = connection.cursor()

        query = "DELETE FROM kitaplar WHERE id = %s"
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
