import sqlite3

def create_db():
    connection = sqlite3.connect('raspa.db')
    cursor = connection.cursor()

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY,
                    group_name TEXT NOT NULL
                    )
                    ''')    

    connection.commit()
    connection.close()