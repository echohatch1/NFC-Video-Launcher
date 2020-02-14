from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os
from threading import Thread
import cv2
import json

#OpenCV Implementation
def open_img():
    img = cv2.imread("assets/images/recycling_home.png")

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
    
    #get card data from json file (hex format)
    data = json.load(open('tagData.json'))
    
    tag_dictionary = data["tags"][0]
        
    while True:
        
        pn532 = Pn532_i2c()
        pn532.SAMconfigure()

        card_data = pn532.read_mifare().get_data().hex()
        
        if card_data != "4b00":
            
            print(card_data)
        
            if card_data in tag_dictionary["tag1"]:
                print("card 1")
                open_vid("assets/video/sample.mp4")
                time.sleep(.1)

            elif card_data in tag_dictionary["tag2"]:
                print("card 2")
                open_vid("assets/video/trash.mp4")
                time.sleep(.1)

            else:
                print("Card not recognized")
                time.sleep(.1)
        time.sleep(1)


if __name__ == '__main__':
    Thread(target = open_img).start()
    Thread(target = read_card).start()
    
    
    #usefull stuff
    #convert bytearray to hex
    #tag1Hex = tag1.hex()
    
    #convert hex to bytearray
    #bytearray.fromhex(tag1Hex)
    
    #store data from json files into variables and convert from hex format
    #tag1 = bytearray.fromhex(data["tag1"][0])
    #tag2 = bytearray.fromhex(data["tag2"][0])
    
    #print (data["tags"][0]["tag1"][0])
    #data_length = len(tag_dictionary)
    
    #for x in range(1, data_length + 1):
        #array_length = len(tag_dictionary["tag" + str(x)])
        #for j in range(0, array_length):
            #print (tag_dictionary["tag" + str(x)][j])
    
    #tag1 = bytearray(b'K\x01\x01\x00\x04\x08\x04W \xdeR')
    #tag2 = bytearray(b'K\x01\x01\x00\x04\x08\x04k\x90]\x1b')