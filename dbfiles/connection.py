import mysql.connector

class DB:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",          
            password="@Tanvi123",
            database="sentiment_db"
        )
        self.cursor = self.mydb.cursor()

    def register_user(self, email, name, password):
        self.cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if self.cursor.fetchone():
            return 0
        else:
            self.cursor.execute('INSERT INTO users (email, name, password) VALUES (%s, %s, %s)', (email, name, password))
            self.mydb.commit()
            return 1

    def login_user(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        return 1 if self.cursor.fetchone() else 0
