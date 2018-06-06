import datetime

class EST5EDT(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime.datetime(dt.year, 3, 8)        #2nd Sunday in March
        self.dston = d + datetime.timedelta(days=6-d.weekday())
        d = datetime.datetime(dt.year, 11, 1)       #1st Sunday in Nov
        self.dstoff = d + datetime.timedelta(days=6-d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'




class Logger:
    def __init__(self, level = None, f = None):
        if level == None:
            self.level = 'Info'
        else:
            self.level = level

        if f == None:
            self.f = 'log.txt'
        else:
            self.f = f

        self.levels = {'System': -1, 'Info': 0, 'Warning': 1, 'Error': 2, 'Fatal': 3}


    def val(self, lvl):
        return self.levels[lvl]


    def log(self, lvl, msg):
        flvl = "[{}]".format(lvl)
        timestamp = "[{}]".format(datetime.datetime.now(tz=EST5EDT()))
        with open(self.f, 'a+') as f:
            f.write("{}{} {}\n".format(flvl, timestamp, msg))

        if self.val(lvl) >= self.val(self.level):
            print("{}{} {}\n".format(flvl, timestamp, msg))



test = Logger(level = 'Warning')
test.log('Info', 'Hello, world!')
