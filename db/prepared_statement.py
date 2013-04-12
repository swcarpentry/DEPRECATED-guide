import sys
import sqlite3

statement = 'select reading from survey where taken=? and quant=?;'

connection = sqlite3.connect('survey.db')
cursor = connection.cursor()
cursor.execute(statement, (int(sys.argv[1]), sys.argv[2]))
for r in cursor.fetchall():
    print r[0]
cursor.close()
connection.close()
