import sqlite3


con = sqlite3.connect('uzmoviebotdb.db')
cur = con.cursor()
from mysql import connector
 
 
# config = {
#     'user':'mirabror',
#     'password':'devmir1998@@',
#     'host':'127.0.0.1',
#     'database':"uzmoviebotdb",
#     "raise_on_warnings":True
# } 
 

# connection = connector.connect(**config)

# cursor = connection.cursor()

# cur.execute('''CREATE TABLE movies(
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         title VARCHAR(300),
#                         country VARCHAR(100),
#                         released_year INT,
#                         language VARCHAR(60),
#                         duration VARCHAR(60),
#                         views_count INT,
#                         banner_link VARCHAR(300),
#                         source_link VARCHAR(300),
#                         category_id INT,
#                         genre_id INT



#                 )''')
# cursor.execute('''DROP TABLE movies''')
# cursor.execute('''SELECT * FROM movies;''')
# cur.execute('''CREATE TABLE users(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     telegram_id INT,
#     first_name VARCHAR(50),
#     last_name VARCHAR(50)
# )''')

# con.close()
# cursor.execute('''SELECT * from movies;''')
# print(cursor.fetchall())
query = (   
        "INSERT INTO movies(id, title, country, released_year, language, duration, views_count, banner_link, source_link)"
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
)
# query = (   
#         "INSERT INTO movies(title, country, released_year, language, duration, views_count, banner_link, source_link)"
#         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
# )
# for q in cursor.fetchall():
#     print(q[0:8])
    # cur.execute(query, q[0:9])
cur.execute('''SELECT * FROM movies  ''')
# print(cur.fetchall())
# cur.execute('''UPDATE  movies SET genre_id=10 WHERE id>6472''')
con.commit()
for i in cur:
    print(i)
con.close()
# connection.commit()
# connection.close()
