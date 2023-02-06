from flask import Flask, render_template, Response, request #flask imports
#from robotLibrary import Robot #import custom made robotLib class for abstraction
from camera import CameraStream #imports "camerastream" class from 'camera.py' file located in the same dir as this app.py file
import cv2 #opencv import

import logging #temp


app = Flask(__name__) #initialize flask object instance
#robot = Robot() #initialize robot class instance
cap = CameraStream().start() #initialize camerastream object instance from other file

#flask run --host=0.0.0.0


#streaming terminal output temp
logging.basicConfig(filename='static/logFile.txt', level=logging.DEBUG, filemode = 'w')



#below is robot-control related endpoints and functions

@app.route("/forward", methods = ['GET','POST'])
def forward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 64))
    timeMS = int(request.args.get('timeMS', default = 1000))
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print(request.environ['REMOTE_ADDR'])
    else:
        print(request.environ['HTTP_X_FORWARDED_FOR']) # if behind a proxy
    print('f')
    #robot.motorForward(speedL, speedR, timeMS)
    return "<p>forward</p>"


@app.route("/backward", methods = ['GET','POST'])
def backward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 66))
    timeMS = int(request.args.get('timeMS', default = 1000))
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print(request.environ['REMOTE_ADDR'])
    else:
        print(request.environ['HTTP_X_FORWARDED_FOR']) # if behind a proxy
    print('b')
    #robot.motorBackward(speedL, speedR, timeMS)
    return "<p>backward</p>"

@app.route("/left", methods = ['GET','POST'])
def left():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850)) 
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print(request.environ['REMOTE_ADDR'])
    else:
        print(request.environ['HTTP_X_FORWARDED_FOR']) # if behind a proxy
    print('l')
    #robot.motorLeft(speedL, speedR, timeMS)
    return "<p>left</p>"

@app.route("/right", methods = ['GET','POST'])
def right():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print(request.environ['REMOTE_ADDR'])
    else:
        print(request.environ['HTTP_X_FORWARDED_FOR']) # if behind a proxy
    print('r')
    #robot.motorRight(speedL, speedR, timeMS)
    return "<p>right</p>"




#below is camera related endpoints and functions

@app.route('/') #main page route
def index(): #main page function
    return render_template('index.html')

def gen_frame(): #generator function, meaning it runs like over and over again and the yield statement at the end instead of being a return it returns a ton over and over looped
    while cap: #maybe equivalent to while true? i mean its just the class instance so idk
        frame = cap.read() #calls class read method
        convert = cv2.imencode('.jpg', frame)[1].tobytes() #sets 'encode' var to a .jpg encoded frame in some fancy byte thing idk its basically encoding the image and yea
        #cv2.waitKey(cap.FPS_MS)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result, idk whats going on here but it seems to just be like sending a frame with a ton of random stuff that i might need to understand later idk

@app.route('/video_feed') #endpoint where raw video feed is streamed
def video_feed():
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') #returns the running of the gen_frame function alongside some html stuff i guess? idk




if __name__ == '__main__': #some sort of thing that makes it so it always runs threaded and on the network but i dont think it works whatever i still run flask run --host=0.0.0.0
    app.run(host='0.0.0.0', threaded=True)