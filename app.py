#flask run --host=0.0.0.0


#regular flask imports
from flask import Flask, render_template, Response, request, redirect, url_for

#below imports are for the authentication system
from flask_sqlalchemy import SQLAlchemy #allows interaction with the sqlite database
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user #allows for user authentication and session management
from flask_wtf import FlaskForm #allows for the creation of forms that will import user information into the database
from wtforms import StringField, PasswordField, SubmitField #allows for the creation of forms that will import user information into the database
from wtforms.validators import InputRequired, Length, ValidationError #allows for the validation of user input in user registration/login forms
from flask_bcrypt import Bcrypt #allows for the hashing of passwords

#below import is custom made robotLib class for abstraction
try:
    from robotLibrary import Robot
except:
    print("robot not connected")

#below imports are for camera
from camera import CameraStream #imports "camerastream" class from 'camera.py' file located in the same dir as this app.py file
import cv2 #opencv import


import time



#object initializations
app = Flask(__name__) #initialize flask app object instance

try:
    robot = Robot() #initialize robot class instance
except:
    print("robot not connected")

cap = CameraStream().start() #initialize camerastream object instance from camera.py file


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #connects the sqlalchemy app to the database file
db = SQLAlchemy(app) #initialize database object instance
app.config['SECRET_KEY'] = 'thisisasecretkey' #used for the encryption of the session cookie

bcrypt = Bcrypt(app)

class User(db.Model, UserMixin): #creates user table in the database
    id = db.Column(db.Integer, primary_key=True) #creates id column, unique identifier for each user
    username = db.Column(db.String(20), nullable=False, unique=True) #username column, limits length to 20 characters and cannot be empty
    password = db.Column(db.String(80), nullable=False) #password column, limits length to 80 characters once hashed and cannot be empty



#clear file on server startup
with open("static/logFile.txt",'w') as logFile:
    logFile.write("Start of Server Session - " + time.strftime("%H:%M:%S", time.localtime()) + "\n")

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

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Forward\n")
    try:
        robot.motorForward(speedL, speedR, timeMS)
    except:
        print("robot not connected")    
    return "<p>forward</p>"

@app.route("/backward", methods = ['GET','POST'])
def backward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 66))
    timeMS = int(request.args.get('timeMS', default = 1000))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Backward\n")
    try:
        robot.motorBackward(speedL, speedR, timeMS)
    except:
        print("robot not connected")    
    return "<p>backward</p>"

@app.route("/left", methods = ['GET','POST'])
def left():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Left\n")
    try:
        robot.motorLeft(speedL, speedR, timeMS)
    except:
        print("robot not connected")    
    return "<p>left</p>"

@app.route("/right", methods = ['GET','POST'])
def right():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Right\n")
    try:
        robot.motorRight(speedL, speedR, timeMS)
    except:
        print("robot not connected")    
    return "<p>right</p>"




#below are real-time movement functions, for use with wasd

@app.route("/stop", methods = ['GET','POST'])
def stop():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Stop\n")
    try:
        robot.motorStop()
    except:
        print("robot not connected")        
    return "<p>stop</p>"

@app.route("/forwardUndef", methods = ['GET','POST'])
def forwardUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Forward Undef\n")
    try:
        robot.motorForwardUndef()
    except:
        print("robot not connected")        
    return "<p>forwardundef</p>"

@app.route("/backwardUndef", methods = ['GET','POST'])
def backwardUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Backward Undef\n")
    try:
        robot.motorBackwardUndef()
    except:
        print("robot not connected")        
    return "<p>backwardundef</p>"

@app.route("/leftUndef", methods = ['GET','POST'])
def leftUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Left Undef\n")
    try:
        robot.motorLeftUndef()
    except:
        print("robot not connected")        
    return "<p>leftundef</p>"

@app.route("/rightUndef", methods = ['GET','POST'])
def rightUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Right Undef\n")
    try:
        robot.motorRightUndef()
    except:
        print("robot not connected")        
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
