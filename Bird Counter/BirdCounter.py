import cv2
import numpy as np
import pandas as pd
import time
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk

directory = r"C:\Users\mjc715\Desktop\Personal Projects\Bird Counter\Bird Pics"
os.chdir(directory)

root = Tk()
root.title("Bird Counter")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Button

startTime = time.time()
cam = cv2.VideoCapture(0)
check, firstFrame = cam.read()
time.sleep(3)
check, firstFrame = cam.read()
ffGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
box = cv2.selectROI(firstFrame)
cv2.destroyAllWindows()

# backSub = cv2.createBackgroundSubtractorMOG2()
# tracker = cv2.TrackerCSRT_create()
i = 0
stop = False

while True:
    ret, frame = cam.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('difference', cv2.absdiff(frameGray, ffGray))
    diffImage = cv2.absdiff(frameGray, ffGray)
    ret, thresh = cv2.threshold(diffImage, 30, 255, cv2.THRESH_BINARY)
    crop = thresh[box[1] : box[1] + box[3], box[0] : box[0] + box[2]]
    whiteness = np.mean(crop)
    cv2.putText(
        frame, str(whiteness), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4
    )
    cv2.imshow("Webcam", frame)

    if whiteness > 50:
        if whiteness > 50 and stop == False:
            filename = "bird" + str(i) + ".jpg"
            cv2.imwrite(filename, frame)
            i += 1
            stop = True
    else:
        stop = False

    # rete = tracker.init(frameGray, box)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.waitKey(1) & 0xFF == ord("r"):
        check, firstFrame = cam.read()
        ffGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)


cam.release()
cv2.destroyAllWindows()
