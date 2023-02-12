from flask import Flask, render_template, Response, request #flask imports
from robotLibrary import Robot #import custom made robotLib class for abstraction
from camera import CameraStream #imports "camerastream" class from 'camera.py' file located in the same dir as this app.py file
import cv2 #opencv import
import time

import logging #temp


app = Flask(__name__) #initialize flask object instance
robot = Robot() #initialize robot class instance
cap = CameraStream().start() #initialize camerastream object instance from other file

#flask run --host=0.0.0.0

#old code, would stream terminal output into logFile
#logging.basicConfig(filename='static/logFile.txt', level=logging.DEBUG, filemode = 'w')




#clear file on server startup
with open("static/logFile.txt",'w') as file:
    pass

#below is the file writing/logging function 
def log(logItem):
    with open("static/logFile.txt", "at") as logFile: #'at' stands for "append text file"
        logFile.write(str(logItem))




#below are precise robot control functions

@app.route("/forward", methods = ['GET','POST'])
def forward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 64))
    timeMS = int(request.args.get('timeMS', default = 1000))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Forward")
    robot.motorForward(speedL, speedR, timeMS)
    return "<p>forward</p>"

@app.route("/backward", methods = ['GET','POST'])
def backward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 66))
    timeMS = int(request.args.get('timeMS', default = 1000))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Backward")
    robot.motorBackward(speedL, speedR, timeMS)
    return "<p>backward</p>"

@app.route("/left", methods = ['GET','POST'])
def left():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Left")
    robot.motorLeft(speedL, speedR, timeMS)
    return "<p>left</p>"

@app.route("/right", methods = ['GET','POST'])
def right():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Right")
    robot.motorRight(speedL, speedR, timeMS)
    return "<p>right</p>"




#below are real-time movement functions, for use with wasd

@app.route("/stop", methods = ['GET','POST'])
def stop():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Stop")
    robot.motorStop()
    return "<p>stop</p>"

@app.route("/forwardUndef", methods = ['GET','POST'])
def forwardUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Forward Undef")
    robot.motorForwardUndef()
    return "<p>forwardundef</p>"

@app.route("/backwardUndef", methods = ['GET','POST'])
def backwardUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Backward Undef")
    robot.motorBackwardUndef()
    return "<p>backwardundef</p>"

@app.route("/leftUndef", methods = ['GET','POST'])
def leftUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Left Undef")
    robot.motorLeftUndef()
    return "<p>leftundef</p>"

@app.route("/rightUndef", methods = ['GET','POST'])
def rightUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Right Undef")
    robot.motorRightUndef()
    return "<p>rightundef</p>"




#below is camera related endpoints and functions

@app.route('/') #main page route
def index(): #main page function
    return render_template('index.html')

def gen_frame(): #generator function, meaning it runs like over and over again and the yield statement at the end instead of being a return it returns a ton over and over looped
    while cap: #maybe equivalent to while true? i mean its just the class instance so idk
        frame = cap.read() #calls class read method
        convert = cv2.imencode('.jpg', frame)[1].tobytes() #sets 'encode' var to a .jpg encoded frame in some fancy byte thing idk its basically encoding the image and yea
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result, idk whats going on here but it seems to just be like sending a frame with a ton of random stuff that i might need to understand later idk

@app.route('/video_feed') #endpoint where raw video feed is streamed
def video_feed():
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') #returns the running of the gen_frame function alongside some html stuff i guess? idk




if __name__ == '__main__': #some sort of thing that makes it so it always runs threaded and on the network but i dont think it works whatever i still run flask run --host=0.0.0.0
    app.run(host='0.0.0.0', threaded=True)
