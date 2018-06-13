import datetime
from tz import EST5EDT




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
