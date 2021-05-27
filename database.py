"""
When setup.py calls us, we should set up the database for this year's
ARRL Field Day contest.
"""

import sqlite3
from datetime import datetime, tzinfo

# Set the database name based on this year.

class DataBase:

    def __init__(self):
        dbname=("fielddaylog-"+str(datetime.utcnow().year)+".db")
        self.conn = sqlite3.connect(dbname)

    def dbsetup(self):
        self.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS qso
                ([qso] INTEGER PRIMARY KEY NOT NULL,
                [utcdatetime] TEXT, [band] TEXT, [mode] TEXT,
                [ocall] TEXT, [ocat] TEXT, [osec] TEXT,
                [tcall] TEXT, [tcat] TEXT, [tsec] TEXT) ''')

        """
        qso - table rows:
            qso - utcdatetime - band - mode - ocall - ocat - osec - tcall - tcat - tsec
        """

    def logwrite(self):
        dt = str(datetime.utcnow())
        self.conn.cursor().execute(''' INSERT INTO qso VALUES(dt, band, mode,
                Ocall, Ocat, Osec, Tcall, Tcat, Tsec) ''')

    def logshow(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM qso")
        print(c.fetchall())

    def logexport(self):
        c = self.conn.cursor()
        c.execute()

        """
        This should create the Cabrillo format export of the logs
        I should figure out how to make DT look like "2021-06-26 1314"
        Or perhaps create a date, and a time table, and only insert
        the simplified values.
        """
def callMethod(o, name):
    return getattr(o, name)()
