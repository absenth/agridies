import sqlite3
from datetime import datetime

year = str(datetime.utcnow().year)
dbname = (f"fielddaylog-{year}.db")
settings = (f"fielddaylog-{year}.settings")


def db_connect():
    """ define database connection """
    con = sqlite3.connect(dbname)
    return con
