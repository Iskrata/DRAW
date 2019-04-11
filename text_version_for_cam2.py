from __future__ import print_function
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib
import time

pl=1
is_game_started = False
print("Player 1")
lower = {'blue':(97, 100, 117)} 
upper = {'blue':(117,255,255)}
colors = {'blue':(255,0,0),
          'red':(0,0,255)}

font = cv2.FONT_HERSHEY_SIMPLEX
first_player_side = (350, 30)
second_player_side = (70, 30)
centered_text = (200, 30)
fontScale = 1
fontColor = (255,255,255)
lineType = 2

number_dots = 0
draw_history_first_player = {}
draw_history_second_player = {}

cam=cv2.VideoCapture(0)

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
                draw_history_first_player[number_dots] = x, y
                print('x:', x, 'y:', y)
        
    for item in draw_history_first_player:
        cv2.circle(frame, (int(draw_history_first_player[item][0]), int(draw_history_first_player[item][1])), 1, colors["red"], 2)


    alpha=0.5
    cv2.line(frame, (330,50), (330,450), (0,0,255), 5)
    cv2.addWeighted(frame, alpha, frame, 0.5, 0, frame)
    frame = cv2.flip(frame, 1)

    if not is_game_started:
        draw_history_first_player = {}
        cv2.putText(frame, 'Type "s" to start the game', second_player_side, font, fontScale, fontColor, lineType)

    if is_game_started:
        cv2.putText(frame, 'The game is started', second_player_side, font, fontScale, fontColor, lineType)

    keys_shortcut = cv2.waitKey(1) & 0xFF
    if keys_shortcut == ord("s"):

        is_game_started = True
        

    cv2.imshow('Player', frame)

    if cv2.waitKey(1)==27:
        cv2.destroyAllWindows()
        break

    keys_shortcut = cv2.waitKey(1) & 0xFF
    if keys_shortcut == ord("r"):
        if pl==1:
            draw_history_first_player={}
        elif pl==2:
            draw_history2={}
    
    if keys_shortcut == ord('q'):
        break

    if keys_shortcut == ord("n"):
        if pl==1:
            pl=2
            print("Player 2")
        else:
            # finish()
            break





