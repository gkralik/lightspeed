# lightspeed

A simple script to measure the internet link speed (using
[sivel/speedtest-cli](https://github.com/sivel/speedtest-cli)) and
save results to a SQlite3 database.

# Setup

*NOTE: Python 3 required.*

Clone the repository and initialize the measurements database.

```
$ git clone https://github.com/gkralik/lightspeed.git

# create database (if not path given, defaults to db/lightspeed.db)
$ python util/create_database.py [path/to/database.db]
```

# Running

Setup a cron job to run `run_test.py` periodically (e.g. every 10 minutes):

```
*/10 * * * *  <your username>  python /path/to/run_test.py
```

# DB Schema

```
CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY,
    pingMs UNSIGNED DECIMAL(10, 3),
    downloadMbit DECIMAL(5, 2),
    uploadMbit DECIMAL(5, 2),
    timestamp DATETIME,
    durationSecs UNSIGNED INTEGER,
    isError INTEGER DEFAULT 0
);
```
