from __future__ import print_function
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib
import time



pp1 = 0
pp2 = 0

wins = [0, 0]

lower = {'blue':(97, 100, 117)} 
upper = {'blue':(117, 255, 255)}
colors = {'blue':(255, 0, 0),
          'red':(0, 0, 255),
          'pink':(153, 51, 255),
          'purple':(166, 26, 155)}

font = cv2.FONT_HERSHEY_SIMPLEX

upper_right_corner = (350, 30)
upper_left_corner = (10, 30)
bottom_right_corner = (500, 450)

centered_text = (200, 30)
fontScale = 1
fontColor = (255,255,255)
lineType = 2
pl = 0

is_game_started = False
is_break_pressed = False
is_game_ended = False

print("Player 1")
number_dots = 0
draw_history = [{}, {}]
cam = cv2.VideoCapture(0)

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
                   


                
    cv2.rectangle(frame, (250,70), (550,250), (255,255,255), 5)
    
    for item in draw_history[pl]:
        cv2.circle(frame, (int(draw_history[pl][item][0]), int(draw_history[pl][item][1])), 3, colors["red"], 6)


    alpha=0.5
    cv2.addWeighted(frame, alpha, frame, 0.5, 0, frame)
    frame = cv2.flip(frame, 1)


    if not is_game_started:
        draw_history[pl]= {}
        cv2.putText(frame, 'Type "s" to start the game', upper_left_corner, font, fontScale, fontColor, lineType)
    
    if is_game_started:
        player_format_text = 'Player {}'.format(str(pl + 1))
        cv2.putText(frame, 'The game is started', upper_left_corner, font, fontScale, fontColor, lineType)
        cv2.putText(frame, player_format_text, bottom_right_corner, font, fontScale, fontColor, lineType)
        
    cv2.imshow('Player', frame)

    if is_break_pressed:
        cv2.destroyAllWindows()
        break

    if is_game_ended:
        
        print("finish")
        cv2.destroyAllWindows()
        img = np.zeros((800, 800, 3), np.uint8)
        img = cv2.rectangle(img, (250, 70), (550, 250), (255, 255, 255), 5)

        
        for i in range(2):
            for item in draw_history[i]:
                x = int(draw_history[i][item][0])
                y = int(draw_history[i][item][1])
                if x<560 and x>240:
                    if y<260 and y>60:
                        if x>535 or x<255 or y>235 or y<75:
                            
                        
                            if i==0:
                                    
                                c="pink"
                                pp1+=1
                                cv2.circle(img, (x, y), 3, colors[c], 6)
                                
                            elif i==1:
                                c="purple"
                                pp2+=1
                                cv2.circle(img, (x, y), 3, colors[c], 6)
                                
                        else:
                            if i==0:
                                c="red"
                            elif i==1:
                                c="blue"
                            cv2.circle(img, (x, y), 3, colors[c], 6)
                            

                    else:
                        if i==0:
                            c="red"
                        elif i==1:
                            c="blue"
                        cv2.circle(img, (x, y), 3, colors[c], 6)
                else:
                    if i==0:
                        c="red"
                    elif i==1:
                        c="blue"
                    cv2.circle(img, (x, y), 3, colors[c], 6)
            
                            
                    
        img = cv2.flip(img, 1)
        cv2.imshow('Results', img)
        cv2.waitKey(1)
        print("Player 1 has {} point".format(pp1))
        print("Player 2 has {} point".format(pp2))
        cv2.putText(img, "Player 1 has {} point".format(str(pp1)), upper_left_corner, font, fontScale, fontColor, lineType)
        #cv2.putText(img, "Player 2 has {} point".format(pp2), upper_left_corner, font, fontScale, fontColor, lineType)
        if pp1>pp2:
            print("Player one wins!")
            #cv2.putText(img, "Player one wins!", upper_left_corner, font, fontScale, fontColor, lineType)
            wins[0]+=1
        elif pp2>pp1:
            print("Player two wins!")
            #cv2.putText(img, "Player two wins!", upper_left_corner, font, fontScale, fontColor, lineType)
            wins[1]+=1
        elif pp1==pp2:
            print("Draw!")
            #cv2.putText(img, "Draw!", upper_left_corner, font, fontScale, fontColor, lineType)

        
        #cv2.destroyAllWindows()
        while not is_break_pressed:
            keys_shortcut = cv2.waitKey(1) & 0xFF
            if keys_shortcut == ord('q'):
                is_break_pressed = True
        break

    keys_shortcut = cv2.waitKey(1) & 0xFF

    if keys_shortcut == ord("s"):
        is_game_started = True

    if keys_shortcut == ord("n"):
        if pl == 0:
            pl = 1
            print("Player 2")

        # elif is_game_ended == True:
        #    is_break_pressed = True
        else:
            is_game_ended = True
            
    if keys_shortcut == ord("r"):
        draw_history[pl]={}

    if cv2.waitKey(1) == 27:
        is_break_pressed = True

    if keys_shortcut == ord('q'):
        is_break_pressed = True
