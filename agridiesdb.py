"""
When setup.py calls us, we should set up the database for this year's
ARRL Field Day contest.
"""

import sqlite3
from datetime import datetime, tzinfo

# Set the database name based on this year.
dbname=("agridieslog-"+str(datetime.today().year)+".db")
conn = sqlite3.connect(dbname)
c = conn.cursor()


def dbsetup():
    c.execute('''CREATE TABLE LOGS
             ([id] INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
             [band] text, [mode] text, [ocall] text, [ocat] text, [osec] text,
             [tcall] text, [tcat] text, [tsec] text, [dt] timestamp)''')

    c.commit()

    '''
    LOGS - table rows:
        band - mode - ocall - ocat - osec - tcall - tcat - tsec - dt
    '''

def logwrite():
    DT = datetime.utcnow()
    c.execute('''INSERT INTO LOGS (band, mode, ocall, ocat, osec, tcall, tcat,
             tsec, dt) VALUES (Band, Mode, Ocall, Ocat, Osec, Tcall, Tcat,
             Tsec, DT)''')

def logshow():
    c.execute("SELECT * FROM LOGS")
    print(c.fetchall())

def logexport():
    '''
    This should create the Cabrillo format export of the logs
    I should figure out how to make DT look like "2021-06-26 1314"
    Or perhaps create a date, and a time table, and only insert
    the simplified values.
    '''
