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

global ROI


def selectFeeder():
    global ROI
    cam = cv2.VideoCapture(0)
    check, firstFrame = cam.read()
    time.sleep(1)
    check, firstFrame = cam.read()
    ROI = cv2.selectROI(firstFrame)
    cv2.destroyAllWindows()
    cam.release()


def start():
    i = 0
    stop = False
    cam = cv2.VideoCapture(0)
    check, firstFrame = cam.read()
    ffGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
    time.sleep(1)
    while True:
        check, frame = cam.read()
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('difference', cv2.absdiff(frameGray, ffGray))
        diffImage = cv2.absdiff(frameGray, ffGray)
        ret, thresh = cv2.threshold(diffImage, 30, 255, cv2.THRESH_BINARY)
        crop = thresh[ROI[1] : ROI[1] + ROI[3], ROI[0] : ROI[0] + ROI[2]]
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


root = Tk()
root.title("Bird Counter")
root.geometry("800x500")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky="NWES")

ttk.Button(mainframe, text="Select Feeder", command=selectFeeder).grid(
    column=1, row=1, sticky="NSWE"
)
ttk.Button(mainframe, text="Start Watch", command=start).grid(
    column=1, row=2, sticky="NSWE"
)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.mainloop()
