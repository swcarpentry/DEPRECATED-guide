import sqlite3

statement = "select site.lat, site.long from site;"

connection = sqlite3.connect("survey.db")
cursor = connection.cursor()
cursor.execute(statement)
for r in cursor.fetchall():
    print r
cursor.close()
connection.close()
