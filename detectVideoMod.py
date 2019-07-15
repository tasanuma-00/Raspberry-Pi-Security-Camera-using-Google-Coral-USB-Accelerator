"""
Taiga Asanuma
7-19-2019
Version 1.0
***Big Credit to Adrian at PyImageSearch for the base code of this file.
		https://www.pyimagesearch.com/2019/04/22/getting-started-with-google-corals-tpu-usb-accelerator/
		https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/

File Description: This is the main file which executes the object detection.
	Boxes will be formed around recognized the objects in the coco_labels.txt
	with a confidence level of over 0.3. Evey second, detected objects and
	the timestamp will be written onto surveillance.txt. If a pre-set object
	is detected, a text message via Pushetta will be sent and record.py 
	is called to record and upload the vidoe to Google Drive. Every hour,
	log.py is called to upload the contents of surveillance.txt to Google
	Drive.
	
"""

# imports
from edgetpu.detection.engine import DetectionEngine
from imutils.video import VideoStream
from PIL import Image
import argparse
import imutils
import cv2

import time
import datetime
from datetime import datetime
from time import strftime

from pushetta import Pushetta

from subprocess import call
import sys


# starting time
start_time = time.time()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to TensorFlow Lite object detection model")
ap.add_argument("-l", "--labels", required=True,
	help="path to labels file")
ap.add_argument("-c", "--confidence", type=float, default=0.3,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the labels dictionary
print("[INFO] parsing class labels...")
labels = {}

# loop over the class labels file
for row in open(args["labels"]):
	# unpack the row and update the labels dictionary
	(classID, label) = row.strip().split(maxsplit=1)
	labels[int(classID)] = label.strip()

# load the Google Coral object detection model
print("[INFO] loading Coral model...")
model = DetectionEngine(args["model"])

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# initializing base variables
sec = -1
prevLabel = []
API_KEY="31549955596bf4c90732ef6c878372b2a3eca83c"
CHANNEL_NAME="RaspiSecurityCamera"
p=Pushetta(API_KEY)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 500 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=1000)
	orig = frame.copy()

	# prepare the frame for object detection by converting (1) it
	# from BGR to RGB channel ordering and then (2) from a NumPy
	# array to PIL image format
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = Image.fromarray(frame)

	# make predictions on the input frame
	start = time.time()
	results = model.DetectWithImage(frame, threshold=args["confidence"],
		keep_aspect_ratio=True, relative_coord=False)
	end = time.time()

	# loop over the results
	for r in results:
		# extract the bounding box and box and predicted class label
		box = r.bounding_box.flatten().astype("int")
		(startX, startY, endX, endY) = box
		label = labels[r.label_id]

		# draw the bounding box and label on the image
		cv2.rectangle(orig, (startX, startY), (endX, endY),
			(0, 255, 0), 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		text = "{}: {:.2f}%".format(label, r.score * 100)
		cv2.putText(orig, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		# appending to surveillance.txt
		file1 = open("surveillance.txt", "a")
		
		# checking if one seccond passed
		if sec != time.strftime("%S"): 								
			target = False;
			# print timestamp
			print(time.ctime()) 											
			file1.write(time.ctime() + "\n")								
			# prints every element in results list
			for r in results:												
				print(labels[r.label_id], end=", ")
				file1.write(labels[r.label_id] + ", ")
				# sets pre-set target element
				if labels[r.label_id] == "cup":								
					target = True
			print("/")
			file1.write("/" + "\n")
			# resets the second to compare
			sec = time.strftime("%S")
			# checks for target element										
			if target:														
				p.pushMessage(CHANNEL_NAME, "The cup has been detected")
				print("recording")
				file1.write("recording")
				vs.stop()
				call(["python3", "record.py"])
				sys.exit()
				
		file1.close()
		
	# checks elapsed time to upload the contents of surveillance.txt
	elapsed_time = time.time() - start_time
	if(elapsed_time > 3600): 
		start_time = time.time()
		print("logging")
		call(["python3", "log.py"])

	# show the output frame and wait for a key press
	cv2.imshow("Frame", orig)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
