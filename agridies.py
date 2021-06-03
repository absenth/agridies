"""
This should serve as the primary mechasim for entering logs on field day
This should ask the user on starup if they need to run the initial setup
scripts.  Perhaps we can check for the existance of a SQLite3 database for this
year and if it exists defaut to no, if it doesn't exist default to yes?

After initial setup, this should take input of "tcall, tcat, tsec" as well
as "band and mode" which after entered should default to the previous values
unless specifically overridden by user input orif we get hamlib/rigctl working
"""

from datetime import datetime
from db_utils import db_connect

""" Set global variables for all the things that need them. """
year = str(datetime.utcnow().year)
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
    """ setup main function """
    if not has_db():
        create_db()

    if not has_settings():
        write_settings()

    while contesting():
        pass


def has_db():
    """ Check for this year's Database """
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cur.fetchall())  # FIXME - add if logic here for qso/settings


def has_settings():
    """ Check for this year's Station Details """
    cur.execute("SELECT callsign FROM station")
    ocall = cur.fetchone()
    if ocall is not None:
        print(f"Have a great field day {ocall}!")
        return True


def create_settings(con, settings):
    """ Function for actually writing station details """
    sql = ''' INSERT INTO station(callsign, category, section)
              VALUES(?, ?, ?) '''
    cur.execute(sql, settings)
    con.commit()
    return cur.lastrowid


def category_check(valueToCheck):
    """ Function to check valid category input """
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
    """ Function to collect station details and push them to the db """
    ocall = input("What is your station callsign: ").upper()
    ocat = input("What is your category: ").upper()
    if not category_check(ocat):
        ocat = input("What is your field day Category?: ").upper()
    osec = input("What is your section: ").upper()

    print(f"Our Call is: {ocall}, Our Cat is: {ocat}, Our Sec is: {osec}")
    settings = (ocall, ocat, osec)
    create_settings(con, settings)


def create_db():
    """ Create our database & Table"""
    cur.execute('''CREATE TABLE IF NOT EXISTS qso
        ([qso] INTEGER PRIMARY KEY NOT NULL, [utcdate] TEXT, [utctime] TEXT,
        [band] TEXT, [mode] TEXT,
        [ocall] TEXT NOT NULL,
        [ocat] TEXT NOT NULL,
        [osec] TEXT NOT NULL,
        [tcall] TEXT NOT NULL,
        [tcat] TEXT NOT NULL,
        [tsec] TEXT NOT NULL)
        ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS station
        ([callsign] TEXT, [category] TEXT, [section] TEXT) ''')

    print(f"Created Database {dbname}")


def contesting():
    """ Get qso details and write them to the database."""
    cur.execute("SELECT callsign, category, section FROM station")
    ocall, ocat, osec = cur.fetchall()[0]

    utcdate = str(datetime.utcnow().date())
    utctime = str(datetime.utcnow().strftime('%H%M'))
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

    qso = (utcdate, utctime, band, mode, ocall, ocat, osec, tcall, tcat, tsec)

    create_qso(con, qso)
    return True


def create_qso(con, qso):
    """ Function for actually writing qso entries, called by getqso()"""
    sql = ''' INSERT INTO qso(utcdate, utctime, band, mode,
                ocall, ocat, osec, tcall, tcat, tsec)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur.execute(sql, qso)
    con.commit()
    return cur.lastrowid


def showlogs(con):
    """ Function to display all logs"""
    cur.execute("SELECT * FROM qso")
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
