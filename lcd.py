#!/usr/bin/env python

from flask import Flask, request, jsonify, send_from_directory
from flask import render_template, request, Response
#from adafruit.Adafruit_PWM_Servo_Driver import PWM
import time
import sys
import picamera
import threading
import os
import io
import gc
import pigpio
import logging
import subprocess

servos = [
    {
        'id': 1,
        'position': 0,
        'gpio' : 23
    },
    {
        'id': 2,
        'position': 0,
        'gpio' : 24
    },
    {
        'id': 3,
        'position': 0,
        'gpio' : 25        
    }
    
]


app = Flask(__name__, static_url_path='/templates');

class AppContext:
    image_mime="image/jpeg";
    image_format="jpeg";
    resp=Response("",  mimetype=image_mime);
    try:
        camera=picamera.PiCamera()
        responded=threading.Event();
        captured=threading.Event();
    except:
        camera = None;
        responded = None;
        captured = None;
        
    def initPigpio(self):
	pi = pigpio.pi()
	if pi.connected:
            self.pi = pi
        else:
            subprocess.Popen("pigpiod")
            time.sleep(20)
            self.pi = pigpio.pi()
        for item in servos:
            self.pi.set_mode(item['gpio'],pigpio.OUTPUT)


    def initAdafruitPWM(self):
        self.pwm = PWM(0x40)
        self.pwm.setPWMFreq(60);

    def __init__(self):
        if (self.camera is not None):
            self.camera.resolution = (400,240)
        self.initPigpio()            

        logging.getLogger("werkzeug").setLevel(logging.ERROR)

        
app_ctx = AppContext();

def captureCam (ioBytes):
    ioBytes.seek(0);
    app_ctx.camera.capture(ioBytes, format=app_ctx.image_format, use_video_port=True,thumbnail=None)
    resp = Response(ioBytes.getvalue(),  mimetype=app_ctx.image_mime);
    resp.headers["Cache-Control"]="no-cache, max-age=0, no-store";

    return (resp);    


def captureCamWorker():
    ioBytes = io.BytesIO();
    resp_next = captureCam(ioBytes);
    while True:
        try:
            app_ctx.resp = resp_next;     
            app_ctx.captured.set();
            resp_next = captureCam(ioBytes);
            app_ctx.responded.wait();            
        finally:
            app_ctx.responded.clear();
            

@app.route('/camera/<path:filename>')
def send_camera(filename):
    if (app_ctx.camera is not None):
        app_ctx.captured.wait();
        resp=app_ctx.resp;
        app_ctx.resp=None;
        app_ctx.captured.clear();
        app_ctx.responded.set();
        return resp;
    else:
        return send_from_directory("assets", "sailboat.jpg",mimetype=app_ctx.image_mime);

            
if (app_ctx.camera is not None):
    t = threading.Thread(target=captureCamWorker);
    t.start();

def rotateServo(servo, angle):
    #app_ctx.pwm.setPWM (servo, 0, int(pulse4096));
    angle = int(angle)
    pw = 1500+(angle*11.111)
    app_ctx.pi.set_servo_pulsewidth(servos[servo]['gpio'], pw)


def rotateServoAdafruit(servo, degree):
    pulse4096 = degree*2.9+370
    app_ctx.pwm.setPWM (servo, 0, int(pulse4096));


for item in servos:
    rotateServo(item['id']-1, item['position'])


@app.route('/assets/<path:filename>')
def send_assets(filename):
    return send_from_directory('assets', filename)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test_dev")
def test_dev_index():
    return render_template('test_dev/index.html')


@app.route('/command/shutdown', methods = ['PUT'])
def command_shutdown():
    os.system("shutdown now");
    return jsonify( { 'status': 0 } )

@app.route('/servos/<int:servo_id>', methods = ['PUT'])
def update_task(servo_id):
    servo = filter(lambda t: t['id'] == servo_id, servos)
    if len(servo) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'position' in request.json and type(request.json['position']) is not int:
        abort(400)
		   
    servo[0]['position'] = request.json.get('position', servo[0]['position'])
    id = servo[0]['id'];
    pos = servo[0]['position']
    rotateServo(id-1,pos);
    return jsonify( { 'task': servo[0] } )

 
if __name__ == "__main__":
#    app.debug = False
    app.run('0.0.0.0', port=80)
