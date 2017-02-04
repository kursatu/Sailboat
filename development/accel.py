import time
import Adafruit_LSM303
from Tkinter import *
import math
import pigpio
from accelerometer import Accelerometer


#lsm303 = Adafruit_LSM303.LSM303()
SERVO_PIN = 23
pi = pigpio.pi()
pi.set_mode(SERVO_PIN, pigpio.OUTPUT)

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.label = Label(frame, text="empty")
        self.label.grid(row=0);
        self.accel = Accelerometer()
			
    def rotateServo(self, angle):
        pw = self.getPulseWidth(angle)
        pi.set_servo_pulsewidth(SERVO_PIN, pw)
        
    # Angle 0-180 degrees
    def getPulseWidth(self, angle):
        angle = int(angle)
        val = 1500+(angle*11.111)
        return val

        '''
    @staticmethod
    def degreeFromRadian(radian):
        val = radian*180/math.pi
        return val
    
    def getInclination(self):
        accel, mag = lsm303.read()
        ax, ay, az = accel
        #sqrtAs = math.sqrt (ax*ax+ay*ay+az*az)
        #axn = ax/sqrtAs
        #ayn = ay/sqrtAs
        print ('Accel X={0}, Accel Y={1}, Accel Z={2}'.format(ax,ay,az))      
        pitchR = math.atan(ax/math.sqrt((ay*ay)+(az*az)))
        pitchD = App.degreeFromRadian(pitchR)
        
        #Roll = arcsin(Ayn/cos(Pitch))
        #roll = math.asin(ayn/math.cos(pitch))
        return pitchD
        
    def getCompassHeading(self):
        accel, mag = lsm303.read()
        accel_x, accel_y, accel_z = accel
        mag_x, mag_z, mag_y = mag
        #print ('Accel X={0}, Accel Y={1}, Accel Z={2}'.format(accel_x,accel_y,accel_z))
        #print ('Mag X={0}, Mag Y={1}, Mag Z={2}'.format(mag_x, mag_y, mag_z))
        val = int(App.degreeFromRadian(math.atan2(mag_x,mag_y)))
        return val
    '''		

    def updateUI(self):
        angle = self.accel.getInclination() #getCompassHeading()
        self.label["text"] = str(angle)
        #self.rotateServo(angle/10+90)
		 
		
def update1():
    root.after(50, update1)
    app.updateUI()
	
		
root = Tk()
root.wm_title('Servo Control')
app = App(root)
root.geometry("200x50+0+0")
root.after(50, update1)
root.mainloop()