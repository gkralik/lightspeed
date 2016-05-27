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
        id INTEGER PRIMARY KEY,
        pingMs UNSIGNED DECIMAL(10, 3),
        downloadMbit DECIMAL(5, 2),
        uploadMbit DECIMAL(5, 2),
        timestamp DATETIME,
        durationSecs UNSIGNED DECIMAL(10, 2),
        isError INTEGER DEFAULT 0
    );
    ''')

    conn.commit()

    print('Database created in', db_path)
except sqlite3.Error as e:
    print('Error:', e.args[0])
finally:
    if conn:
        conn.close()
