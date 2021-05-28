"""
This should serve as the primary mechasim for entering logs on field day
This should ask the user on starup if they need to run the initial setup
scripts.  Perhaps we can check for the existance of a SQLite3 database for this
year and if it exists defaut to no, if it doesn't exist default to yes?

After initial setup, this should take input of "tcall, tcat, tsec" as well
as "band and mode" which after entered should default to the previous values
unless specifically overridden by user input (OR if we get hamlib/rigctl working)
"""

import os.path
import sqlite3
import sys
from datetime import datetime, tzinfo

# Set dbname variable for all the things that need it.
dbname=("fielddaylog-"+str(datetime.utcnow().year)+".db")
band=("14.250") ##FIXME## When hamlib works
mode=("PH") ##FIXME## When hamlib works

def dosetup():
    print("Welcome to Agridies Log")
    print("")
    print("")
    fdsetup = input("Do you need to run the setup? (Yes/No): ").upper()

    if (fdsetup) == "YES":
        eventsetup()
    elif (fdsetup) == "NO":
        print("Checking to see if we need to setup this years Database")
        checkdb()
    else:
        print("I don't know what " + fdsetup +" Means, exiting")
        sys.exit()

def eventsetup():
        Ocall = input("What is your field day callsign?: ").upper
        Ocat = input("What is your field day Category?: ").upper
        Osec = input("What is your ARRL Section?: ").upper
        checkdb()

def checkdb():
    if os.path.isfile(dbname):
        print("Database Exists")
        ##FIXME## Send this to the next funciton.
    else:
        print("Database Doesn't exist, running database setup script")
        dbsetup()

def dbsetup():
    conn = sqlite3.connect(dbname)
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS qso
        ([qso] INTEGER PRIMARY KEY NOT NULL, [utcdatetime] TEXT,
        [band] TEXT, [mode] TEXT, [tcall] TEXT, [tcat] TEXT, [tsec] TEXT) ''')

    print("Created Database " + dbname)
    ##FIXME## Send this to the next function.

def getqso():
    dt = str(datetime.utcnow())
    tcall = input("Their Callsign: ").upper()
    tcat = input("Their Category: ").upper()
    tsec = input("Their Section: ").upper()

    conn = sqlite3.connect(dbname)
    qso = (dt, band, mode, tcall, tcat, tsec)
    create_qso(conn, qso)


def create_qso(conn, qso):
    sql = ''' INSERT INTO qso(utcdatetime, band, mode, tcall, tcat, tsec)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, qso)
    conn.commit()
    return cur.lastrowid


def showlogs():
    conn = sqlite3.connect(dbname)
    conn.cursor().execute("SELECT * FROM qso")
    print(conn.fetchall())

'''
def rigctlsetup():
    #do rigcontrol setup

def showlogs():
    #show all current logs
    #maybe we put this in a separate script?

def exportlogs():
    #create cabrillo format export of logs
    #maybe we put this in a separate script too?
'''

if __name__ == "__main__":
    dosetup()
