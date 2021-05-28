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
                [tcall] TEXT, [tcat] TEXT, [tsec] TEXT) ''')

        """
        qso - table rows:
            qso - utcdatetime - band - mode - tcall - tcat - tsec
        """

    @property
    def utcdatetime(self):
        return self._utcdatetime

    @property
    def band(self):
        return self._band

    @property
    def mode(self):
        return self._mode

    @property


    def logwrite(self):
        self.conn.cursor().execute('INSERT INTO qso VALUES( ?, ?, ?, ?, ?, ?)')

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

        Also, because we're not inserting our callsign, category or section
        into the database with each qso, we will need to construct that as we
        write the Cabrillo export.
        """

def callMethod(o, name):
    return getattr(o, name)()
