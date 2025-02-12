import sqlite3


class SqlLiteDatabase:
    def __init__(self, user_id=None, user_password=None):
        self.conn = None
        
        self.login_user_id = user_id
        self.login_user_password = user_password
        self.login_status = False
        self.connect('test.db')

    def connect(self, database_filename):
        self.conn = sqlite3.connect(database_filename)

    def create_table(self, table_name, columns):
        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' (' + columns + ')')
        self.conn.commit()

    def insert_data(self, table_name, columns, values):
        c = self.conn.cursor()
        placeholders = ', '.join(['?' for _ in values.split(',')])
        c.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', values.split(','))
        self.conn.commit()
        print("Data inserted successfully")

    def fetch_data(self, table_name):
        c = self.conn.cursor()
        c.execute('SELECT * FROM ' + table_name)
        rows_fetched = c.fetchall()
        return rows_fetched

    def delete_data(self, table_name, user_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM ' + table_name + ' WHERE id = ' + user_id)
        self.conn.commit()
        print("Data deleted successfully")
        
    def login_check(self, table_name='users'):
        c = self.conn.cursor()
        c.execute('SELECT * FROM ' + table_name + ' WHERE id = ? AND user_password = ?', (self.login_user_id, self.login_user_password))
        result = c.fetchone()
        if result:
            self.login_status = True
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False

    def fetch_user_data(self, table_name='users'):
        if self.login_status:
            c = self.conn.cursor()
            c.execute('SELECT * FROM ' + table_name + ' WHERE id = ?', (self.login_user_id,))
            result = c.fetchone()
            print("Welcome, ", result[1], "!")
            return result
def log_in():

    user_id_in = input("Enter your user ID: ")
    user_password_in = input("(Don't worry, it's not hack! I am your trusted coach DoubleM!) \n  Enter your password: ")
    sql_database = SqlLiteDatabase(user_id_in, user_password_in)
    while not sql_database.login_check():
        print("Invalid user ID or password. Please try again")
        user_id_in = input("Enter your user ID: ")
        user_password_in = input("Enter your password: ")
        sql_database = SqlLiteDatabase(user_id_in, user_password_in)
    data = sql_database.fetch_user_data()
    return data

