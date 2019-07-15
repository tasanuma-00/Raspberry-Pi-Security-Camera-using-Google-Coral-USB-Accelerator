"""
Taiga Asanuma
7-19-2019
Version 1.0
https://github.com/tasanuma714/Raspberry-Pi-Security-Camera-using-Google-Coral-USB-Accelerator

***Big Credit to Adrian at PyImageSearch for the base code on detectVideoMod.py
	python file.
		https://www.pyimagesearch.com/2019/04/22/getting-started-with-google-corals-tpu-usb-accelerator/
		https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/
    
Description: This python file uploads the contents of surveillance.txt
	after 1 hour and then clears surveillance.txt. This	python file will 
	be called from detectVideoMod.py. You need to be signed into a Google
	Account for the program to work.
	
"""

# imports
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import time


# function for naming text file with timestamp
def get_file_name(): 
    return time.ctime() + ".txt"

# reads and clears content of surveillance.txt
file1 = open("surveillance.txt", "r") 
contents = file1.read()
file1.close()
open('surveillance.txt', 'w').close()

# creates a text file with timestamp
filename2 = get_file_name()
file2 = open(filename2, "w")
file2.write(contents)
file2.close()

# uploads to Google Drive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
file3 = drive.CreateFile()
file3.SetContentFile(filename2)
file3.Upload()
