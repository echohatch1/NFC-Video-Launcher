from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time

import cv2
import numpy as np

# import imageio
# from tkinter import Tk, Label
# from PIL import ImageTk, Image
# from pathlib import Path

# def open_vid():
#     video_name = str(Path().absolute()) + '/sample.mp4'
#     video = imageio.get_reader(video_name)
#     delay = int(1000 / video.get_meta_data()['fps'])

#     def stream(label):

#         try:
#             image = video.get_next_data()
#         except:
#             video.close()
#             return
#         label.after(delay, lambda: stream(label))
#         frame_image = ImageTk.PhotoImage(Image.fromarray(image))
#         label.config(image=frame_image)
#         label.image = frame_image

#     if __name__ == '__main__':

#         root = Tk()
#         my_label = Label(root)
#         my_label.pack()
#         my_label.after(delay, lambda: stream(my_label))
#         root.mainloop()

def open_vid():
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture('sample.mp4')
 
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
 
    # When everything done, release the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

def read_card():
    pn532 = Pn532_i2c()
    pn532.SAMconfigure()
 
    card_data = pn532.read_mifare().get_data()
 
    print(card_data)

    cardOne = bytearray(b'K\x01\x01\x00\x04\x08\x04W \xdeR')
    cardTwo = bytearray(b'K\x01\x01\x00\x04\x08\x04k\x90]\x1b')

    if card_data == cardOne:
        print("card 1")
        open_vid()
        time.sleep(5)
    
    elif card_data == cardTwo:
        print("card 2")
        time.sleep(5)
        
    else:
        print("Card not recognized")
        time.sleep(5)

i = True
while i:
    read_card()