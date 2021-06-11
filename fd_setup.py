from datetime import datetime
from db_utils import db_connect


con = db_connect()
cur = con.cursor()
year = str(datetime.utcnow().year)


def check_for_agridias_database():
    """ See if we have a SQLITE3 database for this year """
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return(cur.fetchall())


def check_for_station_settings():
    """ See if we have set up our station's settings """
    cur.execute("SELECT callsign FROM station")
    our_call = cur.fetchone()
    if our_call is not None:
        return True


def configure_station_settings(con, settings):
    """ Configure our station settings for this year """
    sql = ''' INSERT INTO station(callsign, category, section)
              VALUES(?, ?, ?) '''
    cur.execute(sql, settings)
    con.commit()
    return cur.lastrowid


def configure_agridies_database():
    """ Configure SQLITE3 database for this year """
    cur.execute('''CREATE TABLE IF NOT EXISTS qso
        ([qso] INTEGER PRIMARY KEY NOT NULL, [utcdate] TEXT, [utctime] TEXT,
        [mode] TEXT, [band] TEXT,
        [their_call] TEXT,
        [their_cat] TEXT,
        [their_sec] TEXT,
        ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS station
        ([callsign] TEXT, [category] TEXT, [section] TEXT) ''')

    return True


def write_settings():
    """ Function to collect station details and push them to the db """
    our_call = input("What is your station callsign: ").upper()
    our_cat = input("What is your category: ").upper()
    our_sec = input("What is your section: ").upper()
    settings = (our_call, our_cat, our_sec)
    configure_station_settings(con, settings)
