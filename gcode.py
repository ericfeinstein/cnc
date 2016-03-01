from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import threading

import time
import re
import numpy

filename = 'rachel.xc'
directory = 'gcode/'

print directory+filename

filename = directory+filename

mh = Adafruit_MotorHAT()

speed = 100
steps = 15

x_motor = 1
y_motor = 2

cur_x_pos = 0
cur_y_pos = 0

new_x = 0
new_y = 0

def turnmotor(motor, value):
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
    mystepper.step(int(value), direction,  Adafruit_MotorHAT.SINGLE)

def moveto(x_pos, y_pos, new_x_pos, new_y_pos):
    global cur_x_pos
    global cur_y_pos
    
    x_diff = float(new_x_pos) - float(x_pos)
    y_diff = float(new_y_pos) - float(y_pos)
    #print x_diff
    #print y_diff

    turnmotor(x_motor, x_diff)
    turnmotor(y_motor, y_diff)
        
    cur_x_pos = new_x_pos
    cur_y_pos = new_y_pos
    
def readline(line, cur_x_pos, cur_y_pos):
    if (line[0:3] == 'G02'):
        # Clockwise Arc
        movearc(line, 1, cur_x_pos, cur_y_pos)
    elif (line[0:3] == 'G03'):
        # Counterclockwise Arc
        movearc(line, -1, cur_x_pos, cur_y_pos)
    else:
        for line in lines.split(' '):
        #print line[0]
            
            if (line[0] == 'X'):
                new_x = re.sub("[^0-9.]","",line[1:])
                #print new_x
                
            if (line[0] == 'Y'):
                new_y = re.sub("[^0-9.]","",line[1:])
                #print new_y
        print "move from " + str(cur_x_pos) + "," + str(cur_y_pos) +" to " + str(new_x) + "," + str(new_y)
        moveto(cur_x_pos, cur_y_pos, new_x, new_y)

def movearc(line,direction,x_pos, y_pos):
    global cur_x_pos
    global cur_y_pos
    for item in line.split(' '):            
        if (item[0] == 'X'):
            new_x = re.sub("[^0-9.]","",item[1:])
                #print new_x
        elif (item[0] == 'Y'):
            new_y = re.sub("[^0-9.]","",item[1:])
        elif (item[0] == 'I'): #X offset
            new_i = re.sub("[^0-9.]","",item[1:])
        elif (item[0] == 'J'): #Y offset
            new_j = re.sub("[^0-9.]","",item[1:])
        
        
        x_center=x_pos+new_i   #center of the circle for interpolation
        y_center=y_pos+new_j
           
           
        delta_x=x_pos-x_center
        delta_y=y_pos-y_center      #vector [Dx,Dy] points from the circle center to the new position
           
        r=sqrt(new_j**2+new_i**2);   # radius of the circle
           
        e1=[-new_i,-new_j]; #pointing from center to current position
        if (direction == 1): #clockwise
            e2=[e1[1],-e1[0]];      #perpendicular to e1. e2 and e1 forms x-y system (clockwise)
        else:                   #counterclockwise
            e2=[-e1[1],e1[0]];      #perpendicular to e1. e1 and e2 forms x-y system (counterclockwise)
 
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
 
        no_step=int(round(r*theta/5.0))   # number of point for the circular interpolation
           
        for i in range(1,no_step+1):
            tmp_theta=i*theta/no_step
            tmp_x_pos=xcenter+e1[0]*cos(tmp_theta)+e2[0]*sin(tmp_theta)
            tmp_y_pos=ycenter+e1[1]*cos(tmp_theta)+e2[1]*sin(tmp_theta)
            moveto(cur_x_pos, cur_y_pos, tmp_x_pos, tmp_y_pos)
            cur_x_pos = tmp_x_pos
            cur_y_pos = tmp_y_pos

for lines in open(filename, 'r'):
    #print lines.split(' ')
    line = lines.split(' ')
    line.pop(0) 
    readline(line,cur_x_pos, cur_y_pos)
    

       

def box():
    turnmotor(x_motor,100)
    turnmotor(y_motor,100)
    turnmotor(x_motor,-100)
    turnmotor(y_motor,-100)

moveto(cur_x_pos, cur_y_pos, 0, 0)
