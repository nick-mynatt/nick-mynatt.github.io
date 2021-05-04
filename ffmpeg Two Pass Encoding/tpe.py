# Name: tpe.py
# Author: Nick Mynatt
# Purpose: Use ffmpeg two-pass encoding to give a specific media file size
# Last Modified: 3/17/20

# HOW TO USE:
# In cmd, do:
#   tpe.py [INPUT FILENAME] [SIZE IN MB] [OUTPUT FILENAME]
# 
# Note: use file extensions
# Ex: input.mp4


import os, sys
import ffmpeg

# Command line arguments
# 1. Input filename
# 2. Size in MB
# 3. Output filename
filename = sys.argv[1]
maxSize = int(sys.argv[2])
output_name = sys.argv[3]

filenameList = filename.split('.')
file_format = filenameList[1]

# Size of file in KB
filesize = (maxSize * 8192)

# Getting info from video stream
probe = ffmpeg.probe(filename)
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
duration = float(video_stream['duration'])

# Video bitrate and Audio birate
video_bitrate = filesize / duration
audio_bitrate = 128
video_bitrate -= audio_bitrate
video_bitrate = int(video_bitrate)

os.system("ffmpeg -y -i {0} -c:v libx264 -b:v {2}k -pass 1 -an -f {1} NUL && ^ffmpeg -i {0} -c:v libx264 -b:v {2}k -pass 2 -c:a aac -b:a 128k {3}".format(filename, file_format, video_bitrate, output_name))