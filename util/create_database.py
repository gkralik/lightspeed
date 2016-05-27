#!/usr/bin/env python
import os
import sys
import sqlite3

base_dir = os.path.dirname(os.path.realpath(os.path.join(__file__, '..')))
db_path = os.path.join(base_dir, 'db/lightspeed.db')

if len(sys.argv) == 2:
    db_path = os.path.realpath(sys.argv[1])

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor();

    c.execute('''
    CREATE TABLE IF NOT EXISTS measurements (
        id UNSIGNED INT AUTO_INCREMENT,
        pingMs UNSIGNED DECIMAL(4, 2),
        downloadMbit DECIMAL(4, 2),
        uploadMbit DECIMAL(4, 2),
        createdOn DATETIME,
        PRIMARY KEY (id)
    );
    ''')

    conn.commit()

    print('Database created in', db_path)
except sqlite3.Error as e:
    print('Error:', e.args[0])
finally:
    if conn:
        conn.close()
