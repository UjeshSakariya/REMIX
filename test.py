import sqlite3
connection = sqlite3.connect('users.db', check_same_thread=False)
cursor = connection.cursor()
connection.commit()

##cursor.execute(""" CREATE table comments (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, user TEXT, comment TEXT)""")
cursor.execute('DELETE FROM feed')
connection.commit()
cursor.execute('DELETE FROM comments')
connection.commit()