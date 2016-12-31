import sys
import picamera
import thread
import os
import io
import time

camera=picamera.PiCamera()
camera.resolution = (180,90)

def capture_cam():
    cam_io = io.BytesIO()
    print (time.asctime())
#    try:
#        os.remove('camera/capture.jpg')
#    finally:

#    camera.capture('camera/capture.jpg')
    for n in range (0,100):
        cam_io = io.BytesIO()
        camera.capture(cam_io, format="jpeg", use_video_port=True)
#    file_io = io.FileIO('camera/capture.jpg','w')
#    file_io.write(cam_io.getvalue())
    print (time.asctime())
        
capture_cam()
