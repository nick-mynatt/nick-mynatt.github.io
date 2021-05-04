# Name: CRF_Converter.py
# Author: Nick Mynatt
# Purpose: Compress a video using the CRF function of ffmpeg
# Date: 4/3/20

# How to use
    # Navigate to directory path in terminal, then call:
    #     CRF_Converter.py input.mp4

    # where input.mp4 is the file you want converted

import os, sys

# CRF factor
CRF_CONVERSION_FACTOR = 24

def CRF_Convert(filename):
    os.system("ffmpeg -i \"{0}\" -crf {1} crf_\"{0}\"".format(filename, CRF_CONVERSION_FACTOR))
    
if __name__ == "__main__":
    # Input file
    input_file = sys.argv[1]

    CRF_Convert(input_file)

