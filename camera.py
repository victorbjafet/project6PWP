from threading import Thread, Lock #native python library to allow threading in python programs
import cv2 #opencv import due to camera stuff being used
import time


class CameraStream(object): #camerastream class definition
    def __init__(self, src=0): #camerastream class constructor, src = 0 due to camera ports being ordered by number (0 is first cam plugged in, 1 is second, etc and can do external link sources too)
        self.stream = cv2.VideoCapture(src) #self.stream attribute becomes opencv videocapture 

        #set resolution limits of camera
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        #self.stream.set(cv2.CAP_PROP_FPS, 5) #does not affect anything because it just loops .read lol
        #self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2) #delay, useless tbh but keeping (min 1 max 10)
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        (self.grabbed, self.frame) = self.stream.read() #self.grabbed is boolean ensuring that reading videocapture worked, self.frame is the actual content of the read call
        self.started = False #when object is instantiated set started to false as to prevent double starting somehow thats possible apparently
        self.read_lock = Lock() #something to do with threading cause look at import statement it imports lock from threading

    def start(self): #runs at start of flask program
        if self.started: #checks if self.started attribute is false and stops start sequence if it somehow is
            print("already started!!")
            return None
        self.started = True #if not started already, then set started to true
        self.thread = Thread(target=self.update, args=()) #threading stuff that idk tbh it just works but yea cool it outlines stuff for thread i think
        self.thread.start() #starts thread
        self.framesPassed = 0
        return self #idk why it returns self but it "simply means that your method returns a reference to the instance object on which it was called" and yea idk it works so cool

    def update(self): 
        while self.started:
            (grabbed, frame) = self.stream.read()
            #time.sleep(self.FPS)
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self): #runs like every millisecond cause it runs in the generator function in app.py so yea basically updates the frame each time its run
        self.read_lock.acquire() #thread thing again idk maybe hooks function to seperate thread if i had to guess
        frame = self.frame.copy() #i genuinely dont know refer to 3rd line in constructor and 2nd line in update it has to do with the frame info itself
        self.read_lock.release() #thread thing again woo maybe end thread idfk
        self.framesPassed += 1
        print (self.framesPassed)
        return frame #profit (returns updated frame somehow)

    def stop(self): #sets started to false and i think closes thread too idk too well but likely to prevent process overkill
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback): #runs on program exit
        self.stream.release() #stops stream to prevent it from running in background and hogging processes, opencv thing
