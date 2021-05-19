###
### PACKAGES
###
from datetime import datetime


class NotesPostProcessor:

    myTextFile = None
    durationSlices = []
    firstLineFlag = None
    timeStamps = []
    filePath = None

    def __init__(self, filePath):
        self.firstLineFlag = True
        self.myTextFile = open(filePath, "r")
        self.filePath = filePath

    def parseText(self):
        with self.myTextFile as f:
            for line in f:
                stripped_line = line.strip()
                if self.firstLineFlag:
                    stripped_line = stripped_line[1:]
                    self.firstLineFlag = False
                if len(stripped_line) != 0:
                    if stripped_line[0] == '#':
                        # Arrived at a timestamp, grab it, and store it in seconds
                        temp = self.getTimeStamp(stripped_line)
                        ts = self.convertToSeconds(temp)
                        self.timeStamps.append(ts)
            self.computeDurations()
            # print("TimeStamps: " + str(self.timeStamps))
            # print("Index, start, end, durations: " + str(self.durationSlices))

    def parseTextForSubstrings(self):
        self.myTextFile = open(self.filePath, "r")
        firstHashtag = False
        substring = ''
        substrings = []

        with self.myTextFile as f:
            for line in f:
                index = 0
                while index < len(line):
                    # If you encounter a new section
                    if (line[index] == '#' and (not firstHashtag)):
                        firstHashtag = True
                        # This i++ is to skip the space following the #
                        index += 2
                    elif (line[index] == '#' and firstHashtag):
                        substrings.append(substring)
                        substring = ''
                        # Skip the stop message
                        index += 20
                        firstHashtag = False
                    # If you've started reading this section
                    elif firstHashtag:
                        substring += line[index]
                        index += 1
                    else:
                        index += 1
        return substrings

    def getTimeStamp(self, s):
        title, timeStamp = s.split(':', 1)
        return timeStamp

    def convertToSeconds(self, ts):
        ftr = [3600,60,1]
        if ts.find("PM") == -1:
            ### time is in the morning, convert to seconds normally
            temp = ts.replace("AM", "")
            return sum([a*b for a,b in zip(ftr, map(int, temp.split(':')))])
        else:
            ### time is in afternoon, must add 12 to hour and convert
            temp = ts.replace("PM", "")
            hours, min, sec = temp.split(':')
            hours = str(int(hours) + 12)
            afterNoonTS = hours + ':' + min + ':' + sec
            return sum([a*b for a,b in zip(ftr, map(int, afterNoonTS.split(':')))])

    def checkEven(self):
        if len(self.timeStamps) % 2 == 0:
            return True
        return False

    def computeDurations(self):
        if self.checkEven():
            sliceIndex = 0
            for i in range(1, len(self.timeStamps), 2):
                curr_start = self.timeStamps[i-1]
                curr_end = self.timeStamps[i]
                curr_duration = curr_end - curr_start
                self.durationSlices.append([sliceIndex, curr_start, curr_end, curr_duration])
                sliceIndex += 1
        else:
            #print("There is not an even number of timestamps on the document, current length:" + str(len(self.timeStamps)))
            return -1

###
### Testing
###
# p = NotesPostProcessor("test.txt")

# p.parseText()