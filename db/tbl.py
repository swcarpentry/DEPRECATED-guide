#!/usr/bin/env python
import sys
import sqlite3

if len(sys.argv) == 1:
    statement = sys.stdin.read()
else:
    statement = sys.argv[1]

connection = sqlite3.connect("survey.db")
cursor = connection.cursor()
cursor.execute(statement)
rows = cursor.fetchall()
cursor.close()
connection.close()

if rows:
    width = len(rows[0])
else:
    width = 1

print '  <table class="db">'
print '    <tr>'
print '      <td colspan="%d">' % width
print '<pre>%s</pre>' % statement.strip()
print '      </td>'
print '    </tr>'
for r in rows:
    print '    <tr><td>' + \
          '</td><td>'.join(str(x) for x in r) + \
          '</td></tr>'
print '  </table>'
