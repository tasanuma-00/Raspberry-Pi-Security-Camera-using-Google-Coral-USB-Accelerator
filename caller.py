"""
Taiga Asanuma
7-19-2019
Version 1.0
***Big Credit to Adrian at PyImageSearch for the base code on the child 
	python file	detectVidoeMod.py
		https://www.pyimagesearch.com/2019/04/22/getting-started-with-google-corals-tpu-usb-accelerator/
		https://www.pyimagesearch.com/2019/05/13/object-detection-and-image-classification-with-google-coral-usb-accelerator/
	
Project Description: In this project, I perform object detection on the
	Raspberry Pi using the Google Coral USB Accelerator. A mobilenet_ssd
	_v2_coco_quant_postproces_edgetpu.tflite tensorflow lite model from
	Google is used in my project. This project is modified as a security
	camera, filming a 15-second video and sending a text message via Pushetta
	when a pre-set object from the coco_labels.txt is detected and logging
	the objects detected every second to a text file. Both the video and 
	text file will be uploaded to Google Drive. 
	
Project Dependencies:
	~/python-tflite-source/edgetpu/demo
		caller.py
		detectVideoMod.py
		record.py
		log.py
	~/edgetpu_models/
		mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite
		coco_labels.txt
	
File Description: This is the caller file to perform object detection infinitely
even when the loop the detecVideoTest.py file terminates when a video gets
uploaded to Google Drive.

USAGE: python3 caller.py

"""

# imports
from subprocess  import run	


# infinite loop
while True:				
	print("call")
	# calling detecVideoMod.py
	run(["python3 detectVideoMod.py \
			--model ~/edgetpu_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
			--labels ~/edgetpu_models/coco_labels.txt"], shell=True)
