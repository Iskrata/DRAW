# predi puskane otvarqsh control panel i pishesh:
# pip install opencv-python
# pip install Umat
#pip install imutils
#zaz Umat sigurno shte kaje che lipsva neshto i za vsqko edno posle pishesh
# pip install ...
#... - tova koeto e kazano che lipsva
# moje da probvash dali shte trugna bez Umat i ako trugne moje da ne se svalq
#!!Ako se otvarq s Idle da e otvoren SAMO 1 file shtoto inache dava nqkakva greshka
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib

cam=[]
br=int(input("nqnq: "))
while br>5:
    print("The number of players is too big!")
    br=int(input("nqnq: "))
    
    

def show_webcam(mirror=False):
    #masiv ot prazni prozorci 
    cam.append(cv2.VideoCapture(0))
    
    while True:
        #chete kakvo ima na kamerata i go slaga v promenliva
        #!ako se mahne rval ne raboti! ne znam zashto
        rval, frame = cam[0].read()
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        if mirror:
            #obrushta kamerata
            frame = cv2.flip(frame, 1)

        for key, value in upper.items():
            kernel = np.ones((9,9),np.uint8)
            mask = cv2.inRange(hsv, lower[key], upper[key])
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
           
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
           
                if radius > 25:
                    cv2.circle(frame,
                               (int(x),
                                int(y)),
                               int(radius),
                               colors[key], 2)

 
        for i in range(br):
            #ot i pravi string
            a=str(i+1)
            #pokazva frame-a
            cv2.imshow('nqnq'+a, frame)

        if cv2.waitKey(10) == 27: #izliza ot cikula pri natiskane na esc
            break
    #zatvarq vsichki prozorci
    cv2.destroyAllWindows()



ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())


lower = {'red':(166, 84, 141),
         'green':(66, 122, 129),
         'blue':(97, 100, 117),
         'yellow':(23, 59, 119),
         'orange':(0, 50, 80)}

upper = {'red':(186,255,255),
         'green':(86,255,255),
         'blue':(117,255,255),
         'yellow':(54,255,255),
         'orange':(20,255,255)}
 
colors = {'red':(0,0,255),
          'green':(0,255,0),
          'blue':(255,0,0),
          'yellow':(0, 255, 217),
          'orange':(0,140,255)}




#vika funkciqta kato kazva che e mirrored ekrana i tq go pravi da ne e mirrored
show_webcam(mirror=True)
