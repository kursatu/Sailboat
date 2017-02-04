import Adafruit_LSM303
import math

#lsm303 = Adafruit_LSM303.LSM303()

class Accelerometer(Adafruit_LSM303.LSM303):
      
    @staticmethod
    def degreeFromRadian(radian):
        val = radian*180/math.pi
        return val
    
    def getInclination(self):
        accel, mag = self.read()
        ax, ay, az = accel
        pitchR = math.atan(ax/math.sqrt((ay*ay)+(az*az)))
        pitchD = int(self.degreeFromRadian(pitchR))
        return pitchD
        
    def getCompassHeading(self):
        accel, mag = lsm303.read()
        accel_x, accel_y, accel_z = accel
        mag_x, mag_z, mag_y = mag
        #print ('Accel X={0}, Accel Y={1}, Accel Z={2}'.format(accel_x,accel_y,accel_z))
        #print ('Mag X={0}, Mag Y={1}, Mag Z={2}'.format(mag_x, mag_y, mag_z))
        val = int(Accelerometer.degreeFromRadian(math.atan2(mag_x,mag_y)))
        return val				
			
