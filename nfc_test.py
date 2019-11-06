from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from py532lib.mifare import *
import time
import os
from threading import Thread
import cv2
import numpy as np
import ndef

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
    while True:
#         pn532 = Pn532_i2c()
#         pn532.SAMconfigure()
#         card_data = pn532.read_mifare().get_data()
#         print(card_data)




        #new stuff - to get actual data from card
        card = Mifare()
        card.SAMconfigure()
        card.set_max_retries(MIFARE_SAFE_RETRIES)
        uid = card.scan_field()
        

        if uid:
            
            print([hex(i) for i in uid]) #card uid
            address = card.mifare_address(1,0) #read sector 1 block zero of card
            card.mifare_auth_b(address,MIFARE_FACTORY_KEY)
            data = card.mifare_read(address)
            card.in_deselect() # In case you want to authorize a different sector.
            
            #Example of what the data should look like
#             hexstr = '9101085402656e48656c6c6f5101085402656e576f726c64'
#             octets = bytearray.fromhex(hexstr)
#             print(octets)
            
            print(data) #data in bytearray form
            
            dataArray = [hex(x) for x in data] #data in array form
            print(dataArray)

            time.sleep(5)
            
            #end of new stuff




#         cardOne = bytearray(b'K\x01\x01\x00\x04\x08\x04W \xdeR')
#         cardTwo = bytearray(b'K\x01\x01\x00\x04\x08\x04k\x90]\x1b')
# 
#         if card_data == cardOne:
#             print("card 1")
#             #open_vid("sample.mp4")
# 
#         elif card_data == cardTwo:
#             print("card 2")
#             #open_vid("trash.mp4")
# 
#         else:
#             print("Card not recognized")
#             time.sleep(5)


if __name__ == '__main__':
    #Thread(target = open_img).start()
    Thread(target = read_card).start()
