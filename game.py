import cv2
from time import sleep
import numpy as np
import cvzone
import HandTrackingModule as htm
from pynput.keyboard import Controller
import time
import dictionary
from datetime import datetime

keys = [["G", "H", "E", "M", "A", "O", "."],
        ["BackSpace"]]
finalText = ""

keyboard = Controller()
init_time = time.time()
counter_timeout_text = init_time+1
timer_timeout_text = init_time+1
counter_timeout = init_time+1
timer_timeout = init_time+1


def draw_text(frame, text, x, y, color=(255,0,255), thickness=4, size=3):
    if x is not None and y is not None:
        cv2.putText(frame, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)


def drawAll(img, buttonList):
    for i,button in enumerate(buttonList):
        x, y = button.pos
        w, h = button.size
        
        if i == len(buttonList)-1:
            cvzone.cornerRect(img, (button.pos[0], button.pos[1], 400, button.size[1]),
                          20, rt=0)
            cv2.rectangle(img, button.pos, (x + 400, y + h), (255, 0, 0), cv2.FILLED)

        else:
            cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
            cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if i==0 and j==0:
            buttonList.append(Button([150 * j + 150, 100 * i + 50], key))
        else:
            buttonList.append(Button([150 * j + 150, 100 * i + 50], key))

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.5)
score = 0
timer = 10
counter = 90
i = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    _, img = detector.findHands(img)
    center_x = int(img.shape[0]/2)
    center_y = int(img.shape[0]/2)
    lmList, bboxInfo = detector.findPosition(img)
    if time.time() > timer_timeout_text and timer >0:
        draw_text(img, "Unscramble", center_x-200, center_y, (255,255,255), 8, 5)
        wait2 = 10000
        while wait2 > 0:
            draw_text(img, str(timer), center_x+200, center_y+200, (255,255,255), 8, 5)
            wait2 -= 1
        timer_timeout_text+=0.03333

    elif (time.time() > counter_timeout_text and counter>0):
        img = drawAll(img, buttonList)
        if i == 0:
            counter = counter + 15
        i += 1
        draw_text(img, str(counter), 1150, 70, color = (0,255,255), thickness = 7)
        counter_timeout_text+=0.03333
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                if button.text == "BackSpace":
                    if x < lmList[8][1] < x + w + 400 and y < lmList[8][2] < y + h:
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 350, y + h + 5), (250, 206, 135), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        l, _, _ = detector.findDistance(8, 12, img)

                        ## when clicked
                        if l < 60:
                            cv2.rectangle(img, button.pos, (x + w + 400, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            finalText += button.text
                            sleep(0.15)
                else:
                    if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (250, 206, 135), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        l, _, _ = detector.findDistance(8, 12, img)

                        ## when clicked
                        if l < 60:
                            keyboard.press(button.text)
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            finalText += button.text
                            sleep(0.15)

            
        cv2.rectangle(img, (50, 350), (700, 450), (255, 0, 0), cv2.FILLED)
        if finalText:
            if "BackSpace" in finalText:
                finalText = finalText[:-10]
            cv2.putText(img, finalText, (60, 430),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
            try:
                if finalText[-1] == ".":
                    if finalText[:-1].upper() not in dictionary.op:
                        draw_text(img, "Invalid!!", 200, 600, color = (0,0,255), thickness=7)
                    elif finalText[:-1].upper() in dictionary.op:
                        score += 1
                        finalText = ""
                        cv2.putText(img, finalText, (60, 430),cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                        print(score)
            except:
                pass

        
    if (counter == 0):
        
        wait  = 1000
        while wait > 0:
            draw_text(img, "Time's up", center_x, center_y, color = (0,255,255), thickness = 8)
            draw_text(img, "Your Score is {}".format(score), center_x, center_y+100, color = (0,255,255), thickness = 8)
            wait -= 1
        sleep(0.7)

    if (time.time() > counter_timeout):
        counter-=1
        counter_timeout+=1
    
    if time.time() > timer_timeout:
        #time.sleep(0.5)
        timer-=1
        timer_timeout += 1

        

    cv2.imshow("Image", img)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
    
cap.release()
cv2.destroyAllWindows()
