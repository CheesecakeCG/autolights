import imutils
import cv2
import numpy as np
import time 

isExiting: bool = False
cap = cv2.VideoCapture(0) 
avg_frame = None
delta = None

res = (200, 150)
area = res[0] * res[1]
#  kern = np.ones((10, 10), np.uint8)
kern = (8, 8) 
thres = 3
thresInArea = (thres / 100) * area
timeout = 5
lastHuman = int(time.time()) 

def handleHuman():
    global lastHuman
    print(cv2.countNonZero(delta)/ area, "%")
    if (int(time.time()) > lastHuman + timeout):
        print("TIMED OUT! LIGHTS OUT!")
        lastHuman = float("inf")
        # Turn off the light
        return
    if cv2.countNonZero(delta) > thresInArea:
        print("HUMAN DETECTED AT ", int(time.time())) 
        print("TIMING OUT AT ", int(time.time()) + timeout)
        lastHuman = int(time.time()) + timeout
        # Turn on the light
    

def init():
    global avg_frame
    global delta 
    hasFrame, frame = cap.read()
    avg_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, avg_frame, 1)
    delta = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, delta, 1)
    avg_frame = cv2.resize(avg_frame, res)
    delta = cv2.resize(delta, res)
    pass

def process():
    global avg_frame
    global delta 

    hasFrame, frame = cap.read()
    if not hasFrame:
        return

    # = Pre-process =
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, frame, 1)
    frame = cv2.resize(frame, res)
    #  frame = cv2.dilate(frame, kern)
    frame = cv2.blur(frame, kern)

    # = Ops = 
    delta = avg_frame - frame
    cv2.imshow('unthresh', delta)
    _, delta = cv2.threshold(delta, 10, 255, cv2.THRESH_BINARY, delta)

    handleHuman()
   
    avg_frame = (frame + 15 * avg_frame) / 16 

    # = Display =
    cv2.imshow('Source', frame)
    cv2.imshow('Delta', delta)
    cv2.waitKey(16)


def clean_up():
    cv2.destroyAllWindows()
    cap.release()


def main(): 
    init()
    # === Main Loop ===
    while (not isExiting):
        if (cap.isOpened()):
            process()

    if (isExiting):
        clean_up()


if __name__ == '__main__':
    main()
