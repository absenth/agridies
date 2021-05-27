"""
agridies.py should ask on run "Do you need to run the initial setup"
if the user answers yes, this script should execute.
if the user answers no, we should assume we're already configured for this year
"""
import os.path
from datetime import datetime, tzinfo
from database import DataBase, callMethod
import csv

def checkdb():
    dbname=("fielddaylog-"+str(datetime.utcnow().year)+".db")
    if os.path.isfile(dbname):
        print("DB Exists")
        setstation()
    else:
        print("DB Doesn't exist, running dbsetup")
        database = DataBase()
        callMethod(database, "dbsetup")
        setstation()

def setstation():
    stationfile=("Station.csv")
    if os.path.isfile(stationfile):
        print("Station.csv Exists")
    else:
        Ocall = input("What is your Station Callsign: ").upper()
        Ocat = input("What is your Category: ").upper()
        Osec = input("What is your Section: ").upper()

        Station_Variable=(Ocall, Ocat, Osec)

        with open('Station.csv', 'w', newline = '') as csvfile:
            my_writer = csv.writer(csvfile, delimiter = ' ')
            my_writer.writerow(Station_Variable)
        """
            Will need to write these variables to a file that we can then
            read from databsase.py, for when we write log entries.

            Alternately look into setting up a singleton class.
        """

# Stretch goal - we should hook ourselves up to hamlib/rigctl

if __name__ == '__main__':
    checkdb()
