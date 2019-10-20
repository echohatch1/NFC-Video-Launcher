from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os

#imports for openCV implementation
import cv2
import numpy as np

#display video after scanning
def open_vid(vid):
    command = "omxplayer " + vid
    os.system(command)


#OpenCV Implementation

def open_img():
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture('recycling_home.png')

    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video stream or file")

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            #cv2.imshow('Frame',frame)

            #Display above but full-screen
            cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.imshow("window", frame)


            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break


    
open_img()


def read_card():

    pn532 = Pn532_i2c()
    pn532.SAMconfigure()

    card_data = pn532.read_mifare().get_data()


    print(card_data)

    cardOne = bytearray(b'K\x01\x01\x00\x04\x08\x04W \xdeR')
    cardTwo = bytearray(b'K\x01\x01\x00\x04\x08\x04k\x90]\x1b')

    if card_data == cardOne:
        print("card 1")
        open_vid("sample.mp4")

    elif card_data == cardTwo:
        print("card 2")
        open_vid("trash.mp4")

    else:
        print("Card not recognized")
        time.sleep(5)

i = True
while i:
    read_card()