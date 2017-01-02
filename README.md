# Sailboat

Here is the software I've developed for a remote controlled model sailboat.
The software and the sail boat is in working condition.
I've sailed it many times.
The model sailboat is a monohull (length ~75cm) with a rigid wing sail. 
The rigid wing sail changes its shape by bending 
itself around the midpoint of the chord.

The remote control software is a web application that uses jquery and bootstrap.
It has slider controls for the mainsheet and the rudder.
It also has the a slider for setting the bend angle of the wing sail.
It also displays the camera feed if a camera is present.

There are 2 modes of control
Manual: You need to manually slide the controls.
Tilt: You control by tilting your device. Left/right tilt controls the rudder.
Forward/Backward tilt controls the mainsheet, ie. angle of the wing sail.
The bend angle of the wing sail is not controlled my any tilt, it is usualy 
left at a fixed setting.
The camera slider controls the frame rate. 

The hardware is a raspberrypi 2. It is connected to a adafruit 12 channel servo controller.
The raspberrypi is setup as a wifi hotspot. That way you can connect to it via any device 
and control the boat via a web browser.

Version 2: 
Planned on 1.1.2017
Goals: Make it 3D printable, make the hardware & boat smaller, turn it into a foiling catamaran, 
add a wind direction sensor and accelerometer, use it to adjust wing sail & rudder angle and capsize prevention.  

Status: 
Jan 2, 2017: Ported it to raspberrypi 0 using this article.
https://help.ubuntu.com/community/WifiDocs/WirelessAccessPoint
I had to change up/down events in the interfaces file to add metric for default gateway. 
Otherwise, dual wifi cards would not route.
Replaced adafruit servo controller with pigpio library, eliminating the need for the hardware. 
The servo's still work very well w/o any jitter.






