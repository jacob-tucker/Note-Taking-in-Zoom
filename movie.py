from moviepy.editor import *

"""
movie = "league.mp4"
start_time = 3
end_time = 10
video = VideoFileClip(movie).subclip(start_time,end_time)
name = movie + str(start_time) + "to" + str(end_time) + ".mp4"
video.write_videofile(name)

#audioclip = AudioFileClip("tryout.mp4").subclip(8,14)
#video_with_sound = video.set_audio(audioclip)
"""


#input:
#movie(string), start_time(int - in seconds), end_time(int - in seconds)
#subclip your movie, write result to a file
#webm has sound, mp4 has no sound
def subclip(movie, start_time, end_time):
    video = VideoFileClip(movie).subclip(start_time,end_time)
    video.write_videofile(movie + str(start_time) + "to" + str(end_time) + ".webm")
    
