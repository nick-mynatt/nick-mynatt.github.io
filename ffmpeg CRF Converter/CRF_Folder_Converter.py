# Name: CRF_Folder_Converter.py
# Author: Nick Mynatt
# Purpose: Use CRF_Converter.py on an entire folder
# Date: 4/3/20

# How to use:
    # Navigate to folder you want converted in terminal, then call CRF_Folder_Converter.py


import os, sys
import time
import tkinter as tk
from CRF_Converter import CRF_Convert

# Timer
start_time = time.time()

# Error message
def Error_Box(error_message):
    error = tk.Tk()
    tk.Label(error, text="ERROR: {}".format(error_message)).pack()


# Main variables
func_working = True
dir_path = os.getcwd()
os.chdir(dir_path)
file_list = []

# r = root, d = directories, f = files
for r, d, f in os.walk(dir_path):
    for file in f:
        if '.mp4' in file:
            file_list.append(file)

# Error if file_list is empty
if len(file_list) == 0:
    Error_Box("No files in file_list")
    func_working = False

if func_working:
    for f in file_list:
        CRF_Convert(f)

elapsed_time = time.time() - start_time
print ("\n\n\nTOTAL TIME:\n", str(round(elapsed_time, 2)) + " seconds\n", str(round((elapsed_time/60), 2)) + " minutes\n", str(round((elapsed_time/(60*60)), 2)) + " hours")