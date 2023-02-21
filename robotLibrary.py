# robot class
# need the three lines below each time you write code to power the bot
from adafruit_motorkit import MotorKit

kit = MotorKit(0x40)
import time


class Robot():

    def __init__(self):
        pass

    def motorStop(self):
        kit.motor1.throttle = 0.0
        kit.motor2.throttle = 0.0

    #below methods handle precise, value inputted movement

    def motorForward(self, speedL, speedR, timeMS):
        kit.motor1.throttle = speedL / 100
        kit.motor2.throttle = speedR / 100
        time.sleep(timeMS / 1000)
        self.motorStop()

    def motorBackward(self, speedL, speedR, timeMS):
        kit.motor1.throttle = (speedL / 100) * -1
        kit.motor2.throttle = (speedR / 100) * -1
        time.sleep(timeMS / 1000)
        self.motorStop()

    def motorLeft(self, speedL, speedR, timeMS):
        kit.motor1.throttle = (speedL / 100) * -1
        kit.motor2.throttle = speedR / 100
        time.sleep(timeMS / 1000)
        self.motorStop()

    def motorRight(self, speedL, speedR, timeMS):
        kit.motor1.throttle = speedL / 100
        kit.motor2.throttle = (speedR / 100) * -1
        time.sleep(timeMS / 1000)
        self.motorStop()
    
    #below methods handle real time, perpetual movement for use with wasd

    def motorForwardIndef(self):
        kit.motor1.throttle = 0.5
        kit.motor2.throttle = 0.64
    
    def motorBackwardIndef(self):
        kit.motor1.throttle = -0.5
        kit.motor2.throttle = -0.66

    def motorLeftIndef(self):
        kit.motor1.throttle = -0.5
        kit.motor2.throttle = 0.6

    def motorRightIndef(self):
        kit.motor1.throttle = 0.6
        kit.motor2.throttle = -0.5