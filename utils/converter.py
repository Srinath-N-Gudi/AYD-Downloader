import os
from moviepy.editor import *
from numpy import save
def convert(file_path, save_file_path):
    video = VideoFileClip(file_path)
    video.audio.write_audiofile(os.path.join(save_file_path, file_path.split("/")[-1].replace("mp4", "mp3")), verbose=False, logger=None)
