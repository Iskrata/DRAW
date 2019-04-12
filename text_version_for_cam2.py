from __future__ import print_function
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib
import time
wins=[0,0]
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
pl=0
is_game_started = False
print("Player 1")
number_dots = 0
draw_history=[{},{}]
cam=cv2.VideoCapture(0)

    

def finish(draw1,draw2):
    frame = np.zeros((800,800,3), np.uint8)
    print("finish")
    for i in range(2):
        if i==0:
            c='red'
        elif i==1:
            c='blue'
        for item in draw_history[i]:
            cv2.circle(frame, (int(draw_history[i][item][0]), int(draw_history[i][item][1])), 1, colors[c], 2)


    cv2.putText(frame, "Please vote for the player who is closer ot rectanle's lines", second_player_side, font, fontScale, fontColor, lineType)
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (250,70), (550,250), (255,255,255), 5)
    cv2.imshow('Finish', frame)
    result=int(input("Your vote[1 or 2]: "))
    
    if result==1:
        cv2.destroyAllWindows()
        print("Player one wins!")
        wins[0]+=1
    elif result==2:
        cv2.destroyAllWindows()
        print("Player two wins!")
        wins[1]+=1
    
    print("Game results: ")
    print("Player 1 - ",wins[0], "wins")
    print("Player 2 - ",wins[1], "wins")
   
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
                draw_history[pl][number_dots] = x, y
                #print('x:', x, 'y:', y)
            
    for item in draw_history[pl]:
        cv2.circle(frame, (int(draw_history[pl][item][0]), int(draw_history[pl][item][1])), 1, colors["red"], 2)


    alpha=0.5
    cv2.rectangle(frame, (250,70), (550,250), (255,255,255), 5)
    #cv2.line(frame, (330,50), (330,450), (0,0,255), 5)
    cv2.addWeighted(frame, alpha, frame, 0.5, 0, frame)
    frame = cv2.flip(frame, 1)

    if not is_game_started:
        draw_history[pl]= {}
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
        draw_history[pl]={}
        
    if keys_shortcut == ord('q'):
        cv2.destroyAllWindows()
        break

    if keys_shortcut == ord("n"):
        if pl==0:
            pl=1
            print("Player 2")
        else:
            cv2.destroyAllWindows()
            finish(draw_history[0],draw_history[1])
            break





