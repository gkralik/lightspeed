#!/usr/bin/env python

import os
import re
import sys
import time
from datetime import datetime
import subprocess
import sqlite3


def save_measurement(db_path, ping, download, upload, timestamp, duration, error=False):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        duration = round(duration, 2)

        if error:
            is_error = 1
        else:
            is_error = 0

        c.execute('''INSERT INTO measurements
        (pingMs, downloadMbit, uploadMbit, timestamp, durationSecs, isError)
        VALUES (?, ?, ?, ?, ?, ?)''', (ping, download, upload, timestamp,
                                       duration, is_error))

        conn.commit()
    finally:
        if conn:
            conn.close()


base_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(base_dir, 'db/lightspeed.db')

if len(sys.argv) == 2:
    db_path = os.path.realpath(sys.argv[1])

start = time.time()
start_formatted = datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')

try:
    output = subprocess.check_output(
        [os.path.join(base_dir, 'speedtest-cli', 'speedtest_cli.py'),
         '--simple', '--server', '3199'])
    duration = time.time() - start

    match = re.match(r"Ping:\s(\d+\.\d+)\sms\sDownload:\s(\d+\.\d+)\sMbit/s\sUpload:\s(\d+\.\d+)\sMbit/s",
                     output.decode('utf-8'))
    if match is None:
        raise RuntimeError('returncode is 0 but output match failed')

    save_measurement(db_path, match.group(1), match.group(2),
                     match.group(3), start_formatted, duration)
except subprocess.CalledProcessError as e:
    print('Error: subprocess returned code', e.returncode, '->', e.output)
    save_measurement(db_path, 0, 0, 0, start_formatted,
                     time.time() - start, error=True)

    sys.exit(1)
except RuntimeError as e:
    print('Error:', e)
    save_measurement(db_path, 0, 0, 0, start_formatted, duration, error=True)
    sys.exit(1)
