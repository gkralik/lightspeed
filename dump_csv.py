#!/usr/bin/env python
import os
import sys
import csv
import sqlite3

base_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(base_dir, 'db/lightspeed.db')

if len(sys.argv) == 2:
    db_path = os.path.realpath(sys.argv[1])

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    fieldnames = ['ID', 'Ping (ms)', 'Download (Mbit/s)',
                  'Upload (Mbit/s)', 'Timestamp', 'Duration (s)', 'Error']

    csv = csv.writer(sys.stdout, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    result = c.execute('SELECT * FROM measurements')

    csv.writerow(fieldnames)
    csv.writerows(result)
except sqlite3.Error as e:
    print('Error:', e.args[0])
finally:
    if conn:
        conn.close()
