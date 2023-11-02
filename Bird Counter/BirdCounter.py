import cv2
import numpy as np
import pandas as pd
import time
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk

os.chdir("Bird Counter")
pwd = os.getcwd()
photoDirectory = pwd + "/Bird Pics"
os.chdir("Bird Pics")

global ROI
global cam


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
    global cam
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
                string = datetime.now().strftime("%d/%m, %H:%M")
                filename = string + ".jpg"
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


def exit():
    if "cam" in globals():
        cam.release()
        cv2.destroyAllWindows()
    root.destroy()


root = Tk()
root.title("Bird Catcher")
root.geometry("330x240")
root.resizable(False, False)
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)

ttk.Button(mainframe, text="Select Feeder", command=selectFeeder).grid(column=0, row=1)
ttk.Button(mainframe, text="Start Watch", command=start).grid(column=0, row=2)
ttk.Button(mainframe, text="Exit", command=exit).grid(column=0, row=3)
ttk.Label(mainframe, text="Welcome to Bird Catcher").grid(column=0, row=0)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.mainloop()
