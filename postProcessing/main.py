# imports for google auth and reading arguments
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import sys

# imports for video clipping and watchdog
import postProcessNotes
from moviepy.editor import *
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# google drive auth
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

class Watcher:
		DIRECTORY_TO_WATCH = "../../Documents/Zoom"

		def __init__(self):
				self.observer = Observer()

		def run(self):
				event_handler = Handler()
				self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
				self.observer.start()
				try:
						while True:
								time.sleep(5)
				except:
						self.observer.stop()
						print("Error")

				self.observer.join()


class Handler(FileSystemEventHandler):

		@staticmethod
		def on_created(event):
				if event.is_directory:
						timestamp = event.src_path[event.src_path.find('Zoom')+16:event.src_path.find('Zoom')+24].strip().replace('.', ':')
						print(timestamp)
						# start_time_seconds = ... CONVERT THE TIMESTAMP TO SECONDS HERE

						partialTitle = event.src_path[event.src_path.find('Zoom')+5:]
						title = partialTitle[:partialTitle.find('/')]
						print(title)

# run watchdog
w = Watcher()
w.run()

def doClipping(start_time_seconds, name_of_folder):
	# this gets the text from the google doc in srs.argv[1] and writes it
	# to test.txt
	# sys.argv[1] is the title the google doc you are looking for
	for file_list in drive.ListFile({'q': "title contains '%s'" % str(sys.argv[1])}):
		print('Received %s files from Files.list()' % len(file_list))
		for eachFile in file_list:
			print('title: %s, id: %s' % (eachFile['title'], eachFile['id']))
			file = drive.CreateFile({'id': eachFile['id']})
			file.GetContentFile('test.txt')

	# get all timestamp information
	p = postProcessNotes.NotesPostProcessor("test.txt")
	p.parseText()

	for clip in p.durationSlices:
		subclip("../../Documents/Zoom/" + name_of_folder + "/zoom_0.mp4", clip[1]-start_time_seconds, clip[2]-start_time_seconds, clip[0])

#input:
#movie(string), start_time(int - in seconds), end_time(int - in seconds)
#subclip your movie, write result to a file
def subclip(movie, start_time, end_time, index):
		video = VideoFileClip(movie).subclip(start_time,end_time)
		video.write_videofile(str(index) + "_video.mp4") # CHANGE TO WEBM FOR FINISHED PRODUCT