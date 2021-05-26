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

# import for opening HTML file
import webbrowser
import os.path

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
						startTimeSeconds = get_sec_military(timestamp)
						
						nameOfFolder = event.src_path[event.src_path.find('Zoom')+5:]
						
						doClipping(startTimeSeconds, nameOfFolder)

def get_sec_military(time_str):
	h, m, s = time_str.split(':')
	seconds = int(h) * 3600 + int(m) * 60 + int(s)

	return seconds

def doClipping(start_time_seconds, name_of_folder):
	# this gets the text from the google doc in srs.argv[1] and writes it
	# to test.txt
	# sys.argv[1] is the title the google doc you are looking for
	file_list =  drive.ListFile({'orderBy': "lastViewedByMeDate desc", "maxResults": 1}).GetList()
	docFile = file_list[0]
	print('Received %s files from Files.list()' % len(file_list))
	print('title: %s, id: %s' % (docFile['title'], docFile['id']))
	file = drive.CreateFile({'id': docFile['id']})
	file.GetContentFile('test.txt')

	# get all timestamp information
	p = postProcessNotes.NotesPostProcessor("test.txt")
	p.parseText()


	for clip in p.durationSlices:
		subclip("../../Documents/Zoom/" + name_of_folder + "/zoom_0.mp4", clip[1]-start_time_seconds, clip[2]-start_time_seconds, clip[0])

	# we want to write an html file with python and parse through the text as well
	substrings = p.parseTextForSubstrings()
	createHTML(substrings)

	webbrowser.open_new('file://' + os.path.realpath('index.html'))

#input:
#movie(string), start_time(int - in seconds), end_time(int - in seconds)
#subclip your movie, write result to a file
def subclip(movie, start_time, end_time, index):
		video = VideoFileClip(movie).subclip(start_time,end_time)
		video.write_videofile(str(index) + "_video.mp4") # CHANGE TO WEBM FOR FINISHED PRODUCT

def createHTML(substrings):
	f = open('index.html', 'w')

	sections = ""
	i = 0
	while i < len(substrings):
		newText = substrings[i].split("\n")

		paragraphText = ''
		for j in range(len(newText)):
			paragraphText += newText[j] + "<br>"

		sections += """
		<div class="noteSection">
			<p>{}</p>
			<video id="{}_video" src="./{}_video.mp4" controls></video>
		</div>
		""".format(paragraphText, i, i)
		i += 1

	message = """
	<!DOCTYPE html>
	<html>
	<head>
		<link rel="stylesheet" href="index.css">
		<script type="text/javascript" src="./index.js"></script>
	</head>
	<body>
		<!-- input tag -->
		<input id="searchbar" onkeyup="search_text()" type="text"
			name="search" placeholder="Search notes..">
		<div id="demoContainer">
			{}
		</div>
	</body>
	</html>""".format(sections)

	f.write(message)
	f.close()

# run watchdog
w = Watcher()
w.run()
