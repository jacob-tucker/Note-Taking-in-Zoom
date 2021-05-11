from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import sys

import postProcessNotes

from moviepy.editor import *

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# sys.argv[1] is the title the google doc you are looking for
for file_list in drive.ListFile({'q': "title contains '%s'" % str(sys.argv[1])}):
  print('Received %s files from Files.list()' % len(file_list))
  for eachFile in file_list:
    print('title: %s, id: %s' % (eachFile['title'], eachFile['id']))
    file = drive.CreateFile({'id': eachFile['id']})
    file.GetContentFile('test.txt')

###
### Testing
###
p = postProcessNotes.NotesPostProcessor("test.txt")
p.parseText()



#input:
#movie(string), start_time(int - in seconds), end_time(int - in seconds)
#subclip your movie, write result to a file
def subclip(movie, start_time, end_time, index):
    video = VideoFileClip(movie).subclip(start_time,end_time)
    video.write_videofile(str(index) + "_video.mp4") # CHANGE TO WEBM FOR FINISHED PRODUCT
    
start_time = sys.argv[2]
start_time_seconds = p.convertToSeconds(start_time)
print(start_time_seconds)

for clip in p.durationSlices:
  subclip("demo_class.mp4", clip[1]-start_time_seconds, clip[2]-start_time_seconds, clip[0])

