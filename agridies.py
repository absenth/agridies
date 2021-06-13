

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
from rig_utils import get_riginfo
import npyscreen
# Set global variables for all the things that need them.
year = str(datetime.utcnow().year)
dbname = (f"fielddaylog-{year}.db")
settings = (f"fielddaylog-{year}.settings")

""" setup database extractions """
con = db_connect()
cur = con.cursor()


def main():
    # setup main function 
    if not has_db():
        create_db()
    Application().run()  # starts the application


class Application(npyscreen.NPSAppManaged):
    def onStart(self):
        if not has_settings():   
            '''checking whether there are any settings yet,
             if not, prompt a settings window'''
            self.addForm('MAIN', adjustSettings, name='Welcome to agridies log')
            self.addForm('SECONDARY', mainDisplay, name='Welcome to agridies log')
        else: 
            self.addForm('MAIN', mainDisplay, name='Welcome to agridies log')
            self.addForm('SECONDARY', adjustSettings, name='Welcome to agridies log')


class adjustSettings(npyscreen.ActionForm):
    def afterEditing(self):  
        self.parentApp.getForm('SECONDARY').Ocat.value = self.Ocat.value.upper() 
        #  after the editing is finished, that is, when sbdy presses the ok button,
        #  we want to transfer these values to the main display
        self.parentApp.getForm('SECONDARY').Ocall.value = self.Ocall.value.upper()
        self.parentApp.getForm('SECONDARY').Osec.value = self.Osec.value.upper()
        
        if category_check(self.Ocat.upper):
            self.parentApp.setNextForm('SECONDARY')
            write_settings(self.Ocall.value.upper(), 
                           self.Ocat.value.upper(), self.Osec.value.upper())  # write the settings
            # to the database
        else:
            self.Ocat.value = "You entered a wrong value. Please try again"  
        
    def create(self):
        # asking for the different settings we need
        self.displayValue = show_last_ten_logs()  
        '''the last ten log. Note that they are treated as an array, so passing
        a raw string to them will lead to strange results'''
        self.Entries = self.add(npyscreen.MultiLineEditableBoxed, name='Entries',
                                values=self.displayValue, editable=False, max_height=15, rely=9)
        self.Ocat = self.add(npyscreen.TitleText, name='Enter your category here')
        self.Ocall = self.add(npyscreen.TitleText, name='Enter your station callsign')
        self.Osec = self.add(npyscreen.TitleText, name='Enter your section')
        
        if not category_check(self.Ocat.upper()):  # here we can also implement other validity checks
            self.Ocat.value = 'You entered a wrong value. Please try anew'
                 
        else:
            self.parentApp.Ocat = self.Ocat
            self.parentApp.Ocall = self.Ocall
            self.parentApp.Osec = self.Osec
            settings = (self.Ocall, self.Ocat, self.Osec)
            create_settings(con, settings)


class mainDisplay(npyscreen.Form):

    def afterEditing(self):
        '''the nearest thing i found to a while loop in this context. It calls contesting upon the
        values you entered every time you hit the ok button
        to quit, you simply press ctrl-c. I might also implement a quit yes/no checkbox if wished, or smth of this kind'''
        def contesting():
            """ Get qso details and write them to the database."""
            cur.execute("SELECT callsign, category, section FROM station")
            ocall, ocat, osec = cur.fetchall()[0]

            """ get band and mode data from rig """
            band, mode = get_riginfo()

            utcdate = str(datetime.utcnow().date())
            utctime = str(datetime.utcnow().strftime('%H%M'))
            tcall = self.Tcall.value.upper()
            tcat = self.Tcat.value.upper()
            tsec = self.Tsec.value.upper()

            qso = (utcdate, utctime, band, mode, ocall, ocat, osec, tcall, tcat, tsec)

            create_qso(con, qso)
        contesting()

    def create(self):
        self.displayValue = show_last_ten_logs()
        self.Band = self.add(npyscreen.TitleText, name='Band:')
        self.Mode = self.add(npyscreen.TitleText, name='Mode:')
        self.Entries = self.add(npyscreen.MultiLineEditableBoxed, 
                                name='Entries', values=self.displayValue, editable=False, max_height=15, rely=9)
        self.Ocat = self.add(npyscreen.TitleText, name='Your category',
                             editable=False)  # these values shouldnt be edited
        self.Ocall = self.add(npyscreen.TitleText, name='Your callsign', editable=False)
        self.Osec = self.add(npyscreen.TitleText, name='Your section', editable=False)

        self.Tcat = self.add(npyscreen.TitleText, name='Enter their category', editable=True)
        self.Tcall = self.add(npyscreen.TitleText, name='Enter their callsign', editable=True)
        self.Tsec = self.add(npyscreen.TitleText, name='Enter their section', editable=True)
        
        self.Band.value, self.Mode.value = get_riginfo() 
        
        
def write_settings(Ocall, Ocat, Osec):
    """ Function to collect station details and push them to the db """
    ocall = Ocall
    ocat = Ocat
    osec = Osec

    settings = (ocall, ocat, osec)
    create_settings(con, settings)
   

def has_db():
    """ Check for this year's Database """
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cur.fetchall())  # FIXME - add if logic here for qso/settings


def has_settings():
    """ Check for this year's Station Details """
    cur.execute("SELECT callsign FROM station")
    ocall = cur.fetchone()
    if ocall is not None:
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


def create_db():
    """ Create our database & Table"""
    cur.execute('''CREATE TABLE IF NOT EXISTS qso
        ([qso] INTEGER PRIMARY KEY NOT NULL, [utcdate] TEXT, [utctime] TEXT,
        [mode] TEXT, [band] TEXT,
        [ocall] TEXT NOT NULL,
        [ocat] TEXT NOT NULL,
        [osec] TEXT NOT NULL,
        [tcall] TEXT NOT NULL,
        [tcat] TEXT NOT NULL,
        [tsec] TEXT NOT NULL)
        ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS station
        ([callsign] TEXT, [category] TEXT, [section] TEXT) ''')


def create_qso(con, qso):
    """ Function for actually writing qso entries, called by getqso()"""
    sql = ''' INSERT INTO qso(utcdate, utctime, band, mode,
                ocall, ocat, osec, tcall, tcat, tsec)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur.execute(sql, qso)
    con.commit()
    return cur.lastrowid


'''i was not sure if this function was still needed.
If yes, i might try to implement some kind of keystroke for viewing all
logs. In the current format, it does not work'''


def showlogs(con):  
    """ Function to display all logs"""
    cur.execute("SELECT * FROM qso")
    qsos = cur.fetchall()
    for row in qsos:
        print(row)


def show_last_ten_logs():
    entries = []
    cur.execute('SELECT column FROM qso LIMIT 10')
    qsos = cur.fetchall()
   
    for row in qsos:
        entries.append(row)
    return entries


"""
We still need to setup the export logs feature.
def exportlogs():
    #create cabrillo format export of logs
    #maybe we put this in a separate script too?
"""


if __name__ == "__main__":
    main()
