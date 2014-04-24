import sqlite3
import sys

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.executescript("""
DROP TABLE IF EXISTS Todo;
CREATE TABLE Todo (Name text, Done bool, Priority int, Description text);
INSERT INTO Todo VALUES('WSGI',1, 1, 'Review of WSGI Project');
""")





conn.commit()
conn.close()
