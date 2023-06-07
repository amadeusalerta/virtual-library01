import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Efehan33!",
    database="libraryprogram"
)

def insertProduct(username,userpassword):
 connection=mysql.connector.connect(host="localhost",user="root",password="Efehan33!",database="libraryprogram")
 cursor=connection.cursor()
 
 sql="INSERT INTO users(username,userpassword) VALUES(%s,%s)"
 values=(username,userpassword)

 cursor.execute(sql,values)

 try:
  connection.commit()
  print(f'{cursor.rowcount} unit added')
  print(f'Last Added Unit ID:{cursor.lastrowid}')
 except mysql.connector.Error as Err:
  print('Error:',Err)
 finally:
  connection.close() 
  print("Database connection has closed.")