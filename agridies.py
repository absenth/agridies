"""
This should serve as the primary mechasim for entering logs on field day
This should ask the user on starup if they need to run the initial setup
scripts.  Perhaps we can check for the existance of a SQLite3 database for this
year and if it exists defaut to no, if it doesn't exist default to yes?

After initial setup, this should take input of "tcall, tcat, tsec" as well
as "band and mode" which after entered should default to the previous values
unless specifically overridden by user input orif we get hamlib/rigctl working
"""

import os.path
import sqlite3
import sys
from datetime import datetime

""" Set global variables for all the things that need them. """
year = (str(datetime.utcnow().year))
dbname = (f"fielddaylog-{year}.db")
settings = (f"fielddaylog-{year}.settings")
band = ("14.250")  # FIXME When hamlib works
mode = ("PH")  # FIXME When hamlib works

print("Welcome to Agridies Log\n\n")
print(f"Have a great {year} Field day!\n\n")


def main():
    if not has_db():
        create_db()

    if not has_settings():
        store_settings()

    while contesting():  # FIXME - obviously incomplete
        pass


def has_db():
    """ Check for this year's Database """
    # FIXME - we should turn this into a query for the qso table
    if os.path.isfile(dbname):
        print("Database Exists")
        return True


def has_settings():
    """ Check for this year's Station Details """
    # FIXME - here we need to check the station table for data
    if has_db():
        print("Settings In Place")
        return True


def store_settings(conn, station):
    """ Setup station table write function """
    sql = ''' INSERT INTO station(callsign, category, section)
                VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, station)
    conn.commit()
    return cur.lastrowid

def check(valueToCheck):   #the function I added. I thought it would be better to 
    # create a separate function for this
    equals = False
    numbers = []
    for i in range(1, 21):
        numbers.append(i)
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    for element in numbers:
        for signum in letters:
            if str(element) + signum == valueToCheck:
                equals = True    
    return equals
 

def write_settings():
    """ Get and Write station data into station table """
    ocall = input("What is your field day callsign?: ").upper()
    ocat = input("What is your field day Category?: ").upper()
    if not check(ocat):
        ocat = input("What is your field day Category?: ").upper()  #you have to decide what 
        #actually happens if user enters the wrong category. This would be my suggestion.
    osec = input("What is your ARRL Section?: ").upper()

    conn = sqlite3.connect(dbname)
    station = (ocall, ocat, osec)

    store_settings(conn, station)


def create_db():
    """ Create our database & Table"""
    conn = sqlite3.connect(dbname)
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS qso
        ([qso] INTEGER PRIMARY KEY NOT NULL, [utcdate] TEXT, [utctime] TEXT,
        [band] TEXT, [mode] TEXT, [tcall] TEXT, [tcat] TEXT, [tsec] TEXT,
        [ocall] TEXT, [ocat] TEXT, [osec] TEXT) ''')
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS station
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
            sys.exit()
        elif(exit) == "NO":
            tcall = input("Their Callsign: ").upper()
        else:
            print(f"I'm not sure what {exit} is, but I'm exiting anyway.")
            sys.exit()

    tcat = input("Their Category: ").upper()
    tsec = input("Their Section: ").upper()

    conn = sqlite3.connect(dbname)
    qso = (utcdate, utctime, band, mode, tcall, tcat, tsec, ocall, ocat, osec)

    create_qso(conn, qso)


def create_qso(conn, qso):
    """ Function for actually writing qso entries, called by getqso()"""
    sql = ''' INSERT INTO qso(utcdate, utctime, band, mode,
                tcall, tcat, tsec, ocall, ocat, osec)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, qso)
    conn.commit()
    return cur.lastrowid


def showlogs():
    """ Function to display all logs"""
    conn = sqlite3.connect(dbname)
    conn.cursor().execute("SELECT * FROM qso")
    print(conn.fetchall())
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
