from __future__ import print_function
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib

pl=1
print("Player 1")
lower = {'blue':(97, 100, 117)} 
upper = {'blue':(117,255,255)}
colors = {'blue':(255,0,0)}

number_dots = 0
draw_history = {}
#br=int(input("Number of players: "))

#while br>2:
#    print("The number of players is too big!")
#   br=int(input("Number of players:
cam=cv2.VideoCapture(0)

def finish():
    pass


while True:
    rval, frame = cam.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

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
                number_dots += 1
                draw_history[number_dots] = x, y
        
    for item in draw_history:
        cv2.circle(frame, (int(draw_history[item][0]), int(draw_history[item][1])), 1, colors["red"], 2)


    alpha=0.5
    overlay = frame.copy()
    output= frame.copy()
    cv2.line(overlay, (350,50), (350,450), (0,0,255),5)
    cv2.addWeighted(overlay, alpha, output, 0.5, 0, output)
    output = cv2.flip(output, 1)
    cv2.imshow('Player', output)
    key = cv2.waitKey(1) & 0xFF
    if cv2.waitKey(1)==27:
        cv2.destroyAllWindows()
        break
    if key == ord("r"):
        if pl==1:
            draw_history={}
        elif pl==2:
            draw_history2={}

    if key == ord("n"):
        if pl==1:
            pl=2
            print("Player 2")
        else:
            finish()
            break





