import smtplib
import mysql.connector
from datetime import date

def send_mail():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Efehan33!",
        database="libraryprogram"
    )
    cursor = connection.cursor()

    # Kiralama tablosundan iade tarihi bugün olan kayıtları seçmek için sorgu
    query = "SELECT * FROM kiralama WHERE iade_tarihi = %s"
    current_date = date.today().strftime('%Y-%m-%d')
    cursor.execute(query, (current_date,))
    results = cursor.fetchall()

    # Kullanıcı tablosundan e-posta adresini almak için sorgu
    user_query = "SELECT eposta FROM kullanici WHERE id = %s"

    sender_email = "amogusdrip@gmail.com"
    password = input(str("a33a"))
    message = "Merhaba! Kitaplığımızdan aldığınız kitabın 15 günlük okuma tarihi dolmuştur. Lütfen en kısa süre içerisinde kitabı kitaplığa iade ediniz. Eğer iade etmişseniz bu epostayı dikkate almayınız. Sağlıcakla kalın."

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('amogusdrip@gmail.com',"a33a")
    print("Login success")

    for row in results:
        user_id = row['kullanici_id']
        cursor.execute(user_query, (user_id,))
        user_result = cursor.fetchone()
        rec_email = user_result[0]
        server.sendmail(sender_email, rec_email, message)
        print("Email has been sent to ", rec_email)

    server.quit()

send_mail()
