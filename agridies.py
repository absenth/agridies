"""
This should serve as the primary mechasim for entering logs on field day
This should ask the user on starup if they need to run the initial setup
scripts.  Perhaps we can check for the existance of a SQLite3 database for this
year and if it exists defaut to no, if it doesn't exist default to yes?

After setup this should take input of "their_call, their_cat, their_sec"
as well as "band and mode" read from the transceiver via rigctl.
"""

from datetime import datetime
from db_utils import (
        db_connect,
        show_all_qso,
        create_qso,
        export_cabrillo_log)

from fd_setup import (
        check_for_agridies_database,
        check_for_station_settings,
        configure_agridies_database,
        write_settings)

from rig_utils import get_riginfo

""" Set global variables for all the things that need them. """
year = str(datetime.utcnow().year)
dbname = (f"fielddaylog-{year}.db")
settings = (f"fielddaylog-{year}.settings")

""" setup database extractions """
con = db_connect()
cur = con.cursor()

print("Welcome to Agridies Log\n\n")
print(f"Have a great {year} Field day!\n\n")


def main():
    """ setup main function """
    if not check_for_agridies_database():
        configure_agridies_database()

    if not check_for_station_settings():
        write_settings()

    while contesting():
        pass


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


def contesting():
    """ Get qso details and write them to the database."""
    cur.execute("SELECT callsign, category, section FROM station")
    our_call, our_cat, our_sec = cur.fetchall()[0]

    """ get band and mode data from rig """
    band, mode = get_riginfo()

    utcdate = str(datetime.utcnow().date())
    utctime = str(datetime.utcnow().strftime('%H%M'))
    their_call = input("Their Callsign: ").upper()

    """ Let's see if we can detect no input and use that as an exit criteria"""
    if not their_call:
        print("You didn't enter a callsign.  Do you want to exit?")
        exit = input("YES or NO: ").upper()
        if (exit) == "YES":
            return False
        elif(exit) == "NO":
            their_call = input("Their Callsign: ").upper()
        else:
            print(f"I'm not sure what {exit} is, but I'm exiting anyway.")
            return False

    their_cat = input("Their Category: ").upper()
    their_sec = input("Their Section: ").upper()

    if not category_check(their_cat):
        their_cat = input("Their Category: ").upper()

    qso = (utcdate, utctime, band, mode, their_call, their_cat, their_sec)

    create_qso(con, qso)
    print("")
    return True


if __name__ == "__main__":
    main()
