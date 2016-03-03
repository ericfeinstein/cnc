from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
# import random
import re
from numpy import pi, sin, cos, sqrt, arccos, arcsin
from fractions import gcd

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()



# args

filename = 'rachel_plain.gcode'
directory = 'gcode/'

print directory+filename

filename = directory+filename

speed = 100
steps = 20

x_motor = 1
y_motor = 2

cur_x_pos = 0
cur_y_pos = 0

new_x = 0
new_y = 0


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	# mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	# mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)



# stepstyles = [Adafruit_MotorHAT.SINGLE], Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

style = Adafruit_MotorHAT.SINGLE

def stepper_worker(stepper, numsteps, direction, style):
	#print("Steppin!")
    stepper.step(numsteps, direction, style)
    print "steppin"
	#print("Done")


def turnmotor(motor, value):
    mystepper = mh.getStepper(200,motor)
    if(motor ==1):
        value = -1.0*value
    if(motor ==2):
        value = 1.0*value
    
    if (value <0):
        direction = Adafruit_MotorHAT.BACKWARD
    else:
        direction = Adafruit_MotorHAT.FORWARD
    
    value = abs(value)*steps
    return [int(value), direction, mystepper]

def moveto(x_pos, y_pos, new_x_pos, new_y_pos):
    global cur_x_pos
    global cur_y_pos
    
    # create empty threads (these will hold the stepper 1 and 2 threads)
    st1 = threading.Thread()
    st2 = threading.Thread()

    x_diff = float(new_x_pos) - float(x_pos)
    y_diff = float(new_y_pos) - float(y_pos)
 	#print x_diff
    #print y_diff
    print "move from " + str(x_pos) + "," + str(y_pos) +" to " + str(new_x_pos) + "," + str(new_y_pos)
    steps1 = turnmotor(x_motor, x_diff)
    steps2 = turnmotor(y_motor, y_diff)

# Slow down one motor

    xs = max(abs(x_diff),1)
    ys = max(abs(y_diff),1)
    
    speed_x = speed*xs/max(xs,ys)
    speed_y = speed*ys/max(xs,ys)
    
    steps1[2].setSpeed(speed_x)
    steps2[2].setSpeed(speed_y)
### 
    
    st1 = threading.Thread(target=stepper_worker, args=(steps1[2], steps1[0], steps1[1], Adafruit_MotorHAT.SINGLE))
    st2 = threading.Thread(target=stepper_worker, args=(steps2[2], steps2[0], steps2[1], Adafruit_MotorHAT.SINGLE))
	
    if not st1.isAlive():
        st1.start()
    if not st2.isAlive():
        st2.start()

    while (st1.isAlive() or st2.isAlive()):
        time.sleep(1)
        print "sleepin "
           
    cur_x_pos = new_x_pos
    cur_y_pos = new_y_pos
    
def readline(line, cur_x_pos, cur_y_pos):
    new_x = cur_x_pos
    new_y = cur_y_pos
    print line
    if (line[0] == 'G2'):
        # Clockwise Arc
        print "clockwise arc"
        movearc(line, 1, cur_x_pos, cur_y_pos)
    elif (line[0] == 'G3'):
        print "counter clockwise arc"
        # Counterclockwise Arc
        movearc(line, -1, cur_x_pos, cur_y_pos)
    else:
        print "line"
        for line in lines.split(' '):
        #print line[0]
            
            if (line[0] == 'X'):
                new_x = re.sub("[^0-9.]","",line[1:])
                #print new_x
                
            if (line[0] == 'Y'):
                new_y = re.sub("[^0-9.]","",line[1:])
                #print new_y
#        print "move from " + str(cur_x_pos) + "," + str(cur_y_pos) +" to " + str(new_x) + "," + str(new_y)
        moveto(cur_x_pos, cur_y_pos, new_x, new_y)

def movearc(line,direction,x_pos, y_pos):
    print "arc"
    global cur_x_pos
    global cur_y_pos
    print line
    for item in line:            
        print item
        if (item[0] == 'X'):
            new_x = re.sub("[^0-9.]","",item[1:])
                #print new_x
        elif (item[0] == 'Y'):
            new_y = re.sub("[^0-9.]","",item[1:])
        elif (item[0] == 'I'): #X offset
            new_i = re.sub("[^0-9.]","",item[1:])
        elif (item[0] == 'J'): #Y offset
            new_j = re.sub("[^0-9.]","",item[1:])
        
        
    x_center=float(x_pos)-float(new_i)   #center of the circle for interpolation
    y_center=float(y_pos)-float(new_j)
    print x_center
    print y_center
       
    delta_x=float(x_pos)-float(x_center)
    delta_y=float(y_pos)-float(y_center)     #vector [Dx,Dy] points from the circle center to the new position
       
    r=sqrt(float(new_j)**2+float(new_i)**2);   # radius of the circle
       
    e1=[-float(new_i),-float(new_j)]; #pointing from center to current position
    if (direction == 1): #clockwise
        e2=[-e1[1],e1[0]];      #perpendicular to e1. e2 and e1 forms x-y system (clockwise)
    else:                   #counterclockwise
        e2=[e1[1],-e1[0]];      #perpendicular to e1. e1 and e2 forms x-y system (counterclockwise)

        #[Dx,Dy]=e1*cos(theta)+e2*sin(theta), theta is the open angle

    costheta=(delta_x*e1[0]+delta_y*e1[1])/r**2;
    sintheta=(delta_x*e2[0]+delta_y*e2[1])/r**2;        #theta is the angule spanned by the circular interpolation curve
           
    if costheta>1:  # there will always be some numerical errors! Make sure abs(costheta)<=1
        costheta=1
    elif costheta<-1:
        costheta=-1

    theta=arccos(costheta)
    if sintheta<0:
        theta=2.0*pi-theta

    no_step=10 #int(round(r*theta/5.0))   # number of point for the circular interpolation
       
    for i in range(1,no_step+1):
        tmp_theta=i*theta/no_step
        print 90*theta/3.14
        print 90*tmp_theta/3.14
        tmp_x_pos=x_center+e1[0]*cos(tmp_theta)+e2[0]*sin(tmp_theta)
        print y_center
        print -e1[1]*cos(tmp_theta)
        print -e2[1]*sin(tmp_theta)
        
        
        tmp_y_pos=y_center-e1[1]*cos(tmp_theta)-e2[1]*sin(tmp_theta)
        moveto(cur_x_pos, cur_y_pos, tmp_x_pos, tmp_y_pos)
        cur_x_pos = tmp_x_pos
        cur_y_pos = tmp_y_pos

for lines in open(filename, 'r'):
    #print lines.split(' ')
    line = lines.split(' ')
    line.pop(0)
    if (len(line) > 1):
        readline(line, cur_x_pos, cur_y_pos)
    

       

def box():
    turnmotor(x_motor,100)
    turnmotor(y_motor,100)
    turnmotor(x_motor,-100)
    turnmotor(y_motor,-100)

print "back to origin"
moveto(cur_x_pos, cur_y_pos, 0, 0)

