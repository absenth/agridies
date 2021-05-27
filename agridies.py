"""
This should serve as the primary mechasim for entering logs on field day
This should ask the user on starup if they need to run the initial setup
scripts.  Perhaps we can check for the existance of a SQLite3 database for this
year and if it exists defaut to no, if it doesn't exist default to yes?

After initial setup, this should take input of "tcall, tcat, tsec" as well
as "band and mode" which after entered should default to the previous values
unless specifically overridden by user input (OR if we get hamlib/rigctl working)
"""
import datetime
import eventsetup

def dosetup():
    print("Welcome to Agridies Log")
    print("")
    print("")
    print("Running Initial Setup!")
    eventsetup.checkdb()

if __name__ == '__main__':
    print("dosetup()")
