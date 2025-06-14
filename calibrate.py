import cv2
import numpy as np
from corners import Corners
from deskew import Deskew
from findcontours import FindContour
from train import LaserTracker
import time
import subprocess

window_name = "Calibration"
interframe_wait_ms = 30

cap = cv2.VideoCapture('/dev/video2')
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
while (True):
    ret, frame = cap.read()
    # time.sleep(1)
        # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    crn = Corners(gframe)
    corners = crn.getCorners()
    desk = Deskew(frame, corners)
    frame = desk.deskew()
    # height, width, _ = frame.shape
    # print(height)
    # print(width)
    frame = cv2.resize(frame,(292,382))
    laserTracker = LaserTracker(292, 382)
    # frame = cv2.resize(frame,(int(width),int(1.2562455389*height)))
    # laserTracker = LaserTracker(width, height)
    laser_center = laserTracker.detect(frame)
    if laser_center:
        subprocess.Popen(['aplay', 'gun.wav'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        cv2.circle(frame, laser_center, 3, (0, 0, 255), -1)
        # print(laserTracker.detect(frame))
    fcntr = FindContour(frame, laser_center)
    frame, det = fcntr.findcontour()
    # print (cv2.CAP_PROP_FPS)
    if laser_center and det ==0:
        cv2.circle(frame, laser_center, 3, (0, 0, 255), -1)
        print("Bad shooting, Try again")
    if det == 1:
        # print(cv2.CAP_PROP_POS_FRAME)
        cf = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, cf+200)
        time.sleep(1)
        print("Fire when ready.....")

    # frame = fcntr.findcircle()
    cv2.imshow(window_name, frame)
    if cv2.waitKey(interframe_wait_ms) and cv2.getWindowProperty(window_name,cv2.WND_PROP_VISIBLE) < 1:
        print("Exit requested.")
        break

cap.release()
cv2.destroyAllWindows()
