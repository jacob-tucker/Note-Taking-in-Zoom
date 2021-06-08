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

	# this will store all of the index's of the videos that the html file will need
	# for example if our two videos to be put on the page are 2_video.mp4 and 3_video.mp4, this will
	# hold 2 and 3
	videoNumbers = []
	# make a sublip for each of those videos
	for clip in p.durationSlices:
		videoNumbers.append(subclip("../../Documents/Zoom/" + name_of_folder + "/zoom_0.mp4", clip[1]-start_time_seconds, clip[2]-start_time_seconds))

	# we want to write an html file with python and parse through the text as well
	substrings = p.parseTextForSubstrings()
	htmlIndex = createHTML(substrings, videoNumbers)

	# open the html file in the browser
	webbrowser.open_new('file://' + os.path.realpath('webpages/index_{}.html'.format(htmlIndex)))

#input:
#movie(string), start_time(int - in seconds), end_time(int - in seconds)
#subclip your movie, write result to a file
def subclip(movie, start_time, end_time):
	# making sure to not overwrite previous videos, and then returning the
	# video number we end up using so the corresponding html file can correctly
	# reference it in the video element
	videoNumber = 0
	while True:
		if os.path.exists('videos/{}_video.mp4'.format(videoNumber)):
			videoNumber += 1
		else:
			break
	video = VideoFileClip(movie).subclip(start_time,end_time)
	video.write_videofile("videos/{}_video.mp4".format(videoNumber)) # CHANGE TO WEBM FOR FINISHED PRODUCT FOR AUDIO

	return videoNumber

def createHTML(substrings, videoNumbers):
	# same as the videoNumbers, this makes sure we don't
	# overwrite an existing html page
	htmlPageNumber = 0
	while True:
		if os.path.exists('webpages/index_{}.html'.format(htmlPageNumber)):
			htmlPageNumber += 1
		else:
			break

	# creates a new web page
	f = open('webpages/index_{}.html'.format(htmlPageNumber), 'w')

	# creates each block of notes (the notes with the video corresponding to it)
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
			<video id="{}_video" src="../videos/{}_video.mp4" controls></video>
		</div>
		""".format(paragraphText, videoNumbers[i], videoNumbers[i])
		i += 1

	# the main html structure
	# inserts all the noteSection div blocks using the format
	# string thingy for python
	message = """
	<!DOCTYPE html>
	<html>
	<head>
		<link rel="stylesheet" href="../index.css">
		<script type="text/javascript" src="../index.js"></script>
	</head>
	<body>
		<div id="header">
			<h1>SynchroNote</h1>
			<!-- input tag -->
			<input id="searchbar" onkeyup="search_text()" type="text" name="search" placeholder="Search notes..">
		</div>
		<div id="demoContainer">
			{}
		</div>
	</body>
	</html>""".format(sections)

	f.write(message)
	f.close()

	# return the html page number
	# ex. if our page is index_2.html, we return 2 here
	return htmlPageNumber

# run watchdog
w = Watcher()
w.run()
