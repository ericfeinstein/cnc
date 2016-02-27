from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import threading
mh = Adafruit_MotorHAT()

#500 steps per inch



speed = 200
steps = 50


# X
mystepper = mh.getStepper(200,1)


st1 = threading.Thread()
st2 = threading.Thread()


		

mystepper.setSpeed(speed)
st1 = threading.Thread(target=mystepper.step(steps*10,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))
#_



#Y
mystepper2 = mh.getStepper(200,2)
mystepper2.setSpeed(speed)
## mystepper2.step(steps, 0, Adafruit_MotorHAT.SINGLE)
st2 = threading.Thread(target=mystepper2.step(steps*10, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper2, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))
st2 = threading.Thread(target=mystepper2.step(steps*10, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper2, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))
st2.start()
#|

st3 = threading.Thread(target=mystepper.step(steps*10,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))
#top -

st2 = threading.Thread(target=mystepper2.step(steps*10/3, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper2, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))

#1/4 of |

st1 = threading.Thread(target=mystepper.step(steps*10,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))

#back in

st2 = threading.Thread(target=mystepper2.step(steps*10/3, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper2, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))
#another 1/4

st1 = threading.Thread(target=mystepper.step(steps*10,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))

st2 = threading.Thread(target=mystepper2.step(steps*10/3, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper2, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))
#another 5th
st1 = threading.Thread(target=mystepper.step(steps*10,Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))

st2 = threading.Thread(target=mystepper2.step(steps*10/3, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper2, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))

st1 = threading.Thread(target=mystepper.step(steps*10,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))

st2 = threading.Thread(target=mystepper2.step(steps*10/3, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE), args=(mystepper2, steps*10, 0, Adafruit_MotorHAT.DOUBLE,))

