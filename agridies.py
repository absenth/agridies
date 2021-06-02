"""
This should serve as the primary mechasim for entering logs on field day
This should ask the user on starup if they need to run the initial setup
scripts.  Perhaps we can check for the existance of a SQLite3 database for this
year and if it exists defaut to no, if it doesn't exist default to yes?

After initial setup, this should take input of "tcall, tcat, tsec" as well
as "band and mode" which after entered should default to the previous values
unless specifically overridden by user input orif we get hamlib/rigctl working
"""

import sqlite3
from datetime import datetime
from db_utils import db_connect

""" Set global variables for all the things that need them. """
year = (str(datetime.utcnow().year))
dbname = (f"fielddaylog-{year}.db")
settings = (f"fielddaylog-{year}.settings")
band = ("14.250")  # FIXME When hamlib works
mode = ("PH")  # FIXME When hamlib works

""" setup database extractions """
con = db_connect()
cur = con.cursor()

print("Welcome to Agridies Log\n\n")
print(f"Have a great {year} Field day!\n\n")


def main():
    print("Main")
    """
    if not has_db():
        create_db()

    if not has_settings():
        store_settings()

    while contesting():
        pass
    """


def has_db():
    """ Check for this year's Database """
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cur.fetchall())  # FIXME - add if logic here for qso/settings


def has_settings():
    """ Check for this year's Station Details """
    cur.execute("SELECT station FROM settings")
    print(cur.fetchall())  # FIXME - add if logic here for not-null


def store_settings(con, station):
    """ Setup station table write function """
    settings_sql = ''' INSERT INTO station(callsign, category, section)
                VALUES(?, ?, ?) '''
    cur.execute(settings_sql)
    return cur.lastrowid


def write_settings():
    """ Get and Write station data into station table """
    ocall = input("What is your field day callsign?: ").upper()
    ocat = input("What is your field day Category?: ").upper()
    osec = input("What is your ARRL Section?: ").upper()

    station = (ocall, ocat, osec)
    store_settings(con, station)


def create_db():
    """ Create our database & Table"""
    cur().execute('''CREATE TABLE IF NOT EXISTS qso
        ([qso] INTEGER PRIMARY KEY NOT NULL, [utcdate] TEXT, [utctime] TEXT,
        [band] TEXT, [mode] TEXT, [tcall] TEXT, [tcat] TEXT, [tsec] TEXT,
        [ocall] TEXT, [ocat] TEXT, [osec] TEXT) ''')
    cur().execute('''CREATE TABLE IF NOT EXISTS station
        ([callsign] TEXT, [category] TEXT, [section] TEXT) ''')

    print(f"Created Database {dbname}")


def contesting():
    """ Get qso details and write them to the database."""
    ocall = ()  # FIXME - pull from station table )
    ocat = ()   # FIXME - pull from station table )
    osec = ()   # FIXME - pull from station table )
    utcdate = (str(datetime.utcnow().date()))
    utctime = (str(datetime.utcnow().strftime('%H%M')))
    tcall = input("Their Callsign: ").upper()

    """ Let's see if we can detect no input and use that as an exit criteria"""
    if not tcall:
        print("You didn't enter a callsign.  Do you want to exit?")
        exit = input("YES or NO: ").upper()
        if (exit) == "YES":
            return False
        elif(exit) == "NO":
            tcall = input("Their Callsign: ").upper()
        else:
            print(f"I'm not sure what {exit} is, but I'm exiting anyway.")
            return False

    tcat = input("Their Category: ").upper()
    tsec = input("Their Section: ").upper()

    qso = (utcdate, utctime, band, mode, tcall, tcat, tsec, ocall, ocat, osec)

    create_qso(con, qso)


def create_qso(conn, qso):
    """ Function for actually writing qso entries, called by getqso()"""
    sql = ''' INSERT INTO qso(utcdate, utctime, band, mode,
                tcall, tcat, tsec, ocall, ocat, osec)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur.execute(sql, qso)
    con.commit()
    return cur.lastrowid


def showlogs(con):
    """ Function to display all logs"""
    cur().execute("SELECT * FROM qso")
    print(con.fetchall())
    # FIXME - This is broken


'''
def rigctlsetup():
    #do rigcontrol setup


def exportlogs():
    #create cabrillo format export of logs
    #maybe we put this in a separate script too?
'''


if __name__ == "__main__":
    main()
