"""
Taiga Asanuma
7-19-2019
Version 1.0
***Big Credit to Adrian at PyImageSearch for the base code on detectVideoMod.py
    python file.
        https://www.pyimagesearch.com/2019/04/22/getting-started-with-google-corals-tpu-usb-accelerator/
        https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/
    
File Description: This is the python file which records video after a 
    pre-set object is detected by the detectVideoTest.py. A 15-second 
    video is taken and uploded to Google Drive. This python file will 
	be called from	detectVideoMod.py. You need to be signed into a Google
    Account for the program to work.
    
"""

# imports
import time
import datetime
import picamera

from subprocess import call

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# function for naming video with timestamp
def get_file_name():  
    return time.ctime() + ".h264"
    
# record video
fileName = get_file_name()
cam = picamera.PiCamera()
cam.start_preview()
cam.start_recording(fileName)
time.sleep(15)
cam.stop_preview()
cam.stop_recording() 

# uploads to Google Drive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
file1 = drive.CreateFile()
file1.SetContentFile(fileName)
file1.Upload()
