###
### PACKAGES
###
from datetime import datetime


class NotesPostProcessor:


    myTextFile = None
    durationSlices = []
    firstLineFlag = None
    timeStamps = []

    def __init__(self, filePath):
        self.firstLineFlag = True
        self.myTextFile = open(filePath, "r")

    def parseText(self):
        with self.myTextFile as f:
            for line in f:
                stripped_line = line.strip()
                if self.firstLineFlag:
                    stripped_line = stripped_line[3:]
                    self.firstLineFlag = False
                if len(stripped_line) != 0:
                    if stripped_line[0] == '#':
                        # Arrived at a timestamp, grab it, and store it in seconds
                        temp = self.getTimeStamp(stripped_line)
                        ts = self.convertToSeconds(temp)
                        timeStamps.append(ts)
                        print(ts)
                #print(stripped_line)

    def getTimeStamp(self, s):
        title, timeStamp = s.split(':', 1)
        return timeStamp

    def convertToSeconds(self, ts):
        ftr = [3600,60,1]
        if ts.find("PM") != -1:
            ### time is in the morning, convert to seconds normally
            ts.replace("PM", "")
            ts.strip()
            newTS = '0' + ts
            print(newTS)
            return sum([a*b for a,b in zip(ftr, map(int, newTS.split(':')))])
        else:
            ### time is in afternoon, must add 12 to hour and convert
            ts.replace("AM", "")
            ts.strip()
            hours, min, sec = ts.split(':')
            hours = str(int(hours) + 12)
            afterNoonTS = '0' + hours + ':' + min + ':' + sec
            return sum([a*b for a,b in zip(ftr, map(int, afterNoonTS.split(':')))])




###
### Testing
###

p = NotesPostProcessor("test.txt")
p.parseText()
