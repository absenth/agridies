import sqlite3
from datetime import datetime

year = str(datetime.utcnow().year)
dbname = (f"fielddaylog-{year}.db")
settings = (f"fielddaylog-{year}.settings")


def db_connect():
    """ define database connection """
    con = sqlite3.connect(dbname)
    return con


con = db_connect()
cur = con.cursor()


def show_all_qso():
    """ function to display all qsos """
    cur.execute("SELECT * FROM qso")
    qsos = cur.fetchall()

    for row in qsos:
        print(row)


def export_cabrillo_log():
    """ Function to generate the Cabrillo Format for submitting """
    cur.execute("SELECT * FROM qso")
    qsos = cur.fetchall()

    for row in qsos:
        print(row)
    # FIXME -- this is not the way


def create_qso(con, qso):
    """ Function for actually writing qso entries, called by getqso()"""
    sql = ''' INSERT INTO qso(utcdate, utctime, band, mode,
                their_call, their_cat, their_sec)
                VALUES(?, ?, ?, ?, ?, ?, ?) '''
    cur.execute(sql, qso)
    con.commit()
    return cur.lastrowid
