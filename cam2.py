from __future__ import print_function
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib


lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}
 

colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)} 
number_dots = 0
draw_history = {}
cam=[]
br=int(input("Number of players: "))
while br>2:
    print("The number of players is too big!")
    br=int(input("Number of players: "))

cam.append(cv2.VideoCapture(0))

while True:
    rval, frame = cam[0].read()
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
        cv2.circle(frame, (int(draw_history[item][0]), int(draw_history[item][1])), 1, colors['red'], 2)


    for i in range(br):
        a=str(i+1)
        frame = cv2.flip(frame, 1)
        alpha=0.5
        overlay = frame.copy()
        output= frame.copy()
        cv2.rectangle(overlay, (420, 205), (595, 385),(0, 0, 255), -1)
        cv2.addWeighted(overlay, alpha, output, 0.5, 0, output)
        cv2.imshow('Player'+a, output)
        
    if cv2.waitKey(10) == 27:
        cv2.destroyAllWindows()
        break





