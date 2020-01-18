from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os
from threading import Thread
import cv2
import numpy as np
import json

#OpenCV Implementation
def open_img():
    img = cv2.imread("recycling_home.png")

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    cv2.imshow("window", img)
    
    cv2.waitKey()
    cv2.destroyAllWindows()
    
#display video after scanning
def open_vid(vid):
    command = "omxplayer " + vid
    os.system(command)
    
#listen for nfc cards    
def read_card():
    
    #convert bytearray to hex
    #cardOneHex = cardOne.hex()
    
    #convert hex to bytearray
    #bytearray.fromhex(cardOneHex)
    
    #get card data from json file (hex format)
    data = json.load(open('cardData.json'))
    
    #store data from json files into variables and convert from hex format
    cardOne = bytearray.fromhex(data["cardOne"])
    cardTwo = bytearray.fromhex(data["cardTwo"])
    
    #cardOne = bytearray(b'K\x01\x01\x00\x04\x08\x04W \xdeR')
    #cardTwo = bytearray(b'K\x01\x01\x00\x04\x08\x04k\x90]\x1b')
        
    while True:
        pn532 = Pn532_i2c()
        pn532.SAMconfigure()

        card_data = pn532.read_mifare().get_data()
        
        if card_data != bytearray(b'K\x00'):
            
            print(card_data)
        
            if card_data == cardOne:
                print("card 1")
                open_vid("sample.mp4")      

            elif card_data == cardTwo:
                print("card 2")
                open_vid("trash.mp4")

            else:
                print("Card not recognized")
                time.sleep(5)


if __name__ == '__main__':
    Thread(target = open_img).start()
    Thread(target = read_card).start()
