from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import threading

import time
import re
from numpy import pi, sin, cos, sqrt, arccos, arcsin
from fractions import gcd

filename = 'rachel.gcode'
directory = 'gcode/'

print directory+filename

filename = directory+filename

bottomhat = Adafruit_MotorHAT(addr=0x60)
tophat = Adafruit_MotorHAT(addr=0x61)

mh = bottomhat

speed = 50
steps = 30

x_motor = 1
y_motor = 2
z_motor = 3

cur_x_pos = 0
cur_y_pos = 0
cur_z_pos = 0

new_x = 0
new_y = 0
new_z = 0

def turnmotor(motor, value):
    if (motor == 3):
        mystepper = tophat.getStepper(200,1)
        print "Z ing " + str(value)
    else:
        mystepper = mh.getStepper(200,motor)
    mystepper.setSpeed(speed)
    if(motor ==1):
        value = -1.0*value
    if(motor ==2):
        value = 1.0*value
    
    if (value <0):
        direction = Adafruit_MotorHAT.BACKWARD
    else:
        direction = Adafruit_MotorHAT.FORWARD
    
    value = abs(value)*steps
    mystepper.step(int(value), direction,  Adafruit_MotorHAT.DOUBLE)

def moveto(x_pos, y_pos, new_x_pos, new_y_pos):
    global cur_x_pos
    global cur_y_pos
    
    x_diff = float(new_x_pos) - float(x_pos)
    y_diff = float(new_y_pos) - float(y_pos)
##    m = max(x_diff,y_diff)
##    n = min(x_diff,y_diff)
##    if (n == 0):
##        g = 1
##    else:
##        g = max(x_diff,y_diff)%min(x_diff,y_diff)
##    print "gcd"
##    print g
##    g = int(abs(g))
##    if (g>1):
##        for i in range(1,1+g):
##            print i
##            moveto(float(x_pos)+x_diff/g*(i-1), float(y_pos)+y_diff/g*(i-1), float(new_x_pos)-x_diff/g*(g-i), float(new_y_pos)-y_diff/g*(g-i))

    
    #print x_diff
    #print y_diff
    print "move from " + str(x_pos) + "," + str(y_pos) +" to " + str(new_x_pos) + "," + str(new_y_pos)
    turnmotor(x_motor, x_diff)
    turnmotor(y_motor, y_diff)
        
    cur_x_pos = new_x_pos
    cur_y_pos = new_y_pos


def z_axis(thing):
    if (thing<0):
        turnmotor(z_motor, 1)
    if (thing>0):
        turnmotor(z_motor, -1)
    
    
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
            if (line[0] == 'Z'):
                new_z = re.sub("[^0-9.]","",line[1:])
                z_axis(new_z)
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
        print 180*theta/3.14
        print 180*tmp_theta/3.14
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
