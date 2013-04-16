import sys
import sqlite3

query = "select personal, family from Person where ident='%s';"
user_id = sys.argv[1]

connection = sqlite3.connect("survey.db")
cursor = connection.cursor()

cursor.execute(query % user_id)
results = cursor.fetchall()
print results[0][0], results[0][1]

cursor.close()
connection.close()
