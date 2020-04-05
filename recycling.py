from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os
from threading import Thread
import cv2
import json
from tkinter import *
from PIL import Image, ImageTk

#omxplayer-wrapper
from omxplayer.player import OMXPlayer
from pathlib import Path

global deviceValue
deviceValue = "trash"

# #OpenCV Implementation
# def open_img():
#     img = cv2.imread("assets/images/recycling_home.png")
# 
#     cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
#     cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
#     
#     cv2.imshow("window", img)
#     
#     cv2.waitKey()
#     cv2.destroyAllWindows()

#tkinter Implementation
#def open_img():
#     global root
#     root=Tk()
#     root.geometry('1600x900')
#     root.title('Preparing')
#     root.attributes('-fullscreen', True)
# 
#     imge=Image.open('assets/images/recycling_home_resized.png')
#     photo=ImageTk.PhotoImage(imge)
# 
#     lab=Label (image=photo)
#     lab.pack()
#     
#     root.mainloop()


def open_img():
    global player
    player = OMXPlayer('assets/video/wait_test.mp4', args='--loop')
    sleep(5)
    
#display video after scanning
def open_vid(vid):
#     command = "omxplayer " + vid
#     os.system(command)

    #omxplayer-wrapper
    player = OMXPlayer(vid)
    sleep(5)
    player.quit()
    
#listen for nfc cards    
def read_card():
    
    #get card data from json file (hex format)
#     data = json.load(open('tagData.json'))
#     data.close()
    
    jsonFile = open("shared/tagData.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    tag_dictionary = data["tags"]
    list_keys = list(tag_dictionary.keys())
       
    while True:
        pn532 = Pn532_i2c()
        pn532.SAMconfigure()
        
        card_data = pn532.read_mifare().get_data().hex()
        
        if card_data != "4b00":
            
            print(card_data)
            player.quit()
            
            for i in list_keys:
                if card_data in tag_dictionary[i]["uids"]:
                    print(i)
                    if i != "killtag":
                        if deviceValue == tag_dictionary[i]["category"]:
                            open_vid("assets/video/" + tag_dictionary[i]["category"] + ".mp4")
                            open_img()
                            break
                        else:
                            open_vid("assets/video/wrong.mp4")
                            open_img()
                            break
                    else:
                        print("closing")
                        #command = "python3 add_tag.py"
                        #os.system(command)
                        #read_card()
                        #root.destroy()
                        break


            else:
                print("Card not recognized")
                command = "python3 admin.py " + str(card_data)
                os.system(command)
                read_card()
                #time.sleep(.5)
                #continue

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