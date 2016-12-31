#!/usr/bin/env python

#from flask import Flask, request, jsonify, send_from_directory
#from flask import render_template, request, Response
from adafruit.Adafruit_PWM_Servo_Driver import PWM
from bottle import route,run, template, Response, static_file
import time
import sys
import picamera
import threading
import os
import io
import gc


servos = [
    {
        'id': 1,
        'position': -25
    },
    {
        'id': 2,
        'position': 25
    }
]


#app = Flask(__name__, static_url_path='/templates')


class AppContext:
    resp=Response("",  mimetype='image/jpeg');
    camera=picamera.PiCamera()
    pwm = PWM(0x40)
    responded=threading.Event();
    captured=threading.Event();    
    def __init__(self):
        self.camera.resolution = (400,240)
        self.pwm.setPWMFreq(60);
        
app_ctx = AppContext();

def captureCam (ioBytes):
    ioBytes.seek(0);
    app_ctx.camera.capture(ioBytes, format="jpeg", use_video_port=True)
    resp = Response(ioBytes.getvalue(),  content_type='image/jpeg');
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
            

@route('/camera/<filename>')
def send_camera(filename):
    app_ctx.captured.wait();
    resp=app_ctx.resp;
    app_ctx.resp=None;
    app_ctx.captured.clear();
    app_ctx.responded.set();
    
    return resp;
            

t = threading.Thread(target=captureCamWorker);
t.start();
    
def rotateServo(servo, degree):
    pulse4096 = degree*1.9+340
    app_ctx.pwm.setPWM (servo, 0, int(pulse4096));

for item in servos:
    rotateServo(item['id']-1, item['position'])


@route('/assets/<filename:path>')
def send_assets(filename):
    return static_file(filename, root='assets')

@route("/")
def index():
    return template('base')

@route("/test_dev")
def test_dev_index():
    return render_template('test_dev/index.html')

"""
@route('/servos/<int:servo_id>', methods = ['PUT'])
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
"""
 
if __name__ == "__main__":
#    app.debug = False
    run(host='0.0.0.0', port=80)
