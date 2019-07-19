# Raspberry-Pi-Security-Camera-using-Google-Coral-USB-Accelerator

In this project, I perform object detection on the
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
