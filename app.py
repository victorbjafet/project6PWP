#command to run server on network: flask run --host=0.0.0.0

import time

#regular flask imports
from flask import Flask, render_template, Response, request, redirect, url_for

#auth imports
from flask_sqlalchemy import SQLAlchemy #allows interaction with the sqlite database
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user #allows for user authentication and session management
from flask_wtf import FlaskForm #allows for the creation of forms that will import user information into the database
from wtforms import StringField, PasswordField, SubmitField #allows for the creation of forms that will import user information into the database
from wtforms.validators import InputRequired, Length, ValidationError #allows for the validation of user input in user registration/login forms
from flask_bcrypt import Bcrypt #allows for the hashing of passwords

#import custom made robotLibrary class for abstraction (from robotLibrary.py)
robotConnected = True
try:
    from robotLibrary import Robot
except:
    print("Robot not connected")
    robotConnected = False

#camera imports 
from camera import CameraStream #imports "camerastream" class from 'camera.py' file located in the same dir as this app.py file
import cv2 #opencv import



#object instantiations
app = Flask(__name__) #creates flask app instance
cap = CameraStream().start() #initialize camerastream object instance from camera.py
try:
    robot = Robot() #initialize robot class instance
except:
    pass


#auth instances
bcrypt = Bcrypt(app) #creates bcrypt instance for hashing passwords
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #route to database file (needs to be before sqlalchemy instance)
app.config['SECRET_KEY'] = 'thisisasecretkey' #secret key for session management
db = SQLAlchemy(app) #creates sqlalchemy instance in order to interact with database
login_manager = LoginManager() #creates login manager instance from flask_login
login_manager.init_app(app) #initializes login manager
login_manager.login_view = 'login' #sets login route 


@login_manager.user_loader #loads user from database when user is logged in
def load_user(user_id):
    return User.query.get(int(user_id))

#creates database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

#creates form for registering a user
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

#creates form for logging in user
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



#clear file on server startup
with open("static/logFile.txt",'w') as logFile:
    logFile.write("Start of Server Session - " + time.strftime("%H:%M:%S", time.localtime()) + "\n")

#below is the file writing/logging function 
def log(logItem):
    with open("static/logFile.txt", "at") as logFile: #'at' stands for "append text file"
        logFile.write(str(logItem))



@app.route('/dashboard', methods=['GET', 'POST']) #main page that displays all the important stuff, can only be accessed when logged in
@login_required
def dashboard():
    return render_template('dashboard.html')

#below endpoints all have to do with auth
#just add @login_required to any route you want to protect
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




#below are precise robot control functions

@app.route("/forward", methods = ['GET','POST'])
@login_required
def forward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 64))
    timeMS = int(request.args.get('timeMS', default = 1000))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Forward\n")
    if robotConnected == True:
        robot.motorForward(speedL, speedR, timeMS)
    return "<p>forward</p>"

@app.route("/backward", methods = ['GET','POST'])
@login_required
def backward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 66))
    timeMS = int(request.args.get('timeMS', default = 1000))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Backward\n")
    if robotConnected == True:
        robot.motorBackward(speedL, speedR, timeMS)
    return "<p>backward</p>"

@app.route("/left", methods = ['GET','POST'])
@login_required
def left():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Left\n")
    if robotConnected == True:
        robot.motorLeft(speedL, speedR, timeMS)
    return "<p>left</p>"

@app.route("/right", methods = ['GET','POST'])
@login_required
def right():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))

    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Right\n")
    if robotConnected == True:
        robot.motorRight(speedL, speedR, timeMS)
    return "<p>right</p>"




#below are real-time movement functions, for use with wasd

@app.route("/stop", methods = ['GET','POST'])
@login_required
def stop():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Stop\n")
    if robotConnected == True:
        robot.motorStop()
    return "<p>stop</p>"

@app.route("/forwardUndef", methods = ['GET','POST'])
@login_required
def forwardUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Forward Undef\n")
    if robotConnected == True:
        robot.motorForwardUndef()
    return "<p>forwardundef</p>"

@app.route("/backwardUndef", methods = ['GET','POST'])
@login_required
def backwardUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Backward Undef\n")
    if robotConnected == True:
        robot.motorBackwardUndef()
    return "<p>backwardundef</p>"

@app.route("/leftUndef", methods = ['GET','POST'])
@login_required
def leftUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Left Undef\n")
    if robotConnected == True:
        robot.motorLeftUndef()
    return "<p>leftundef</p>"

@app.route("/rightUndef", methods = ['GET','POST'])
@login_required
def rightUndef():
    log(str(request.environ['REMOTE_ADDR']) + " - " + time.strftime("%H:%M:%S", time.localtime()) + " | Right Undef\n")
    if robotConnected == True:
        robot.motorRightUndef()
    return "<p>rightundef</p>"




#below is camera related endpoints and functions

def gen_frame(): #generator function, meaning it runs like over and over again and the yield statement at the end instead of being a return it returns a ton over and over looped
    while cap: #maybe equivalent to while true? i mean its just the class instance so idk
        frame = cap.read() #calls class read method
        convert = cv2.imencode('.jpg', frame)[1].tobytes() #sets 'encode' var to a .jpg encoded frame in some fancy byte thing idk its basically encoding the image and yea
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result, idk whats going on here but it seems to just be like sending a frame with a ton of random stuff that i might need to understand later idk

@app.route('/video_feed') #endpoint where raw video feed is streamed
@login_required
def video_feed():
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') #returns the running of the gen_frame function alongside some html stuff i guess? idk




if __name__ == '__main__': #some sort of thing that makes it so it always runs threaded and on the network but i dont think it works whatever i still run flask run --host=0.0.0.0
    app.run(host='0.0.0.0', threaded=True)
