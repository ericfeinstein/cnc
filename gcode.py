from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import threading

import time
import re

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
    

for lines in open(filename, 'r'):
    #print lines.split(' ')
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

       

def box():
    turnmotor(x_motor,100)
    turnmotor(y_motor,100)
    turnmotor(x_motor,-100)
    turnmotor(y_motor,-100)

moveto(cur_x_pos, cur_y_pos, 0, 0)
