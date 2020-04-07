from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os
from threading import Thread
import json
from tkinter import *
from omxplayer.player import OMXPlayer
from pathlib import Path

global deviceValue
#set to "trash", "compost", or "recycling"
deviceValue = "trash"

def open_background():
    global root
    root=Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='grey')
    root.mainloop()

def open_main_vid():
    global player
    player = OMXPlayer('assets/video/wait_' + deviceValue + '.mp4', args='--loop')
    sleep(2.5)
    
#display video after scanning
def open_vid(vid, vid_length):
    player = OMXPlayer(vid)
    sleep(vid_length)
    player.quit()
    
#listen for nfc cards    
def read_card():
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
                            open_vid("assets/video/" + tag_dictionary[i]["category"] + ".mp4", 14)
                            open_main_vid()
                            break
                        else:
                            open_vid("assets/video/wrong.mp4", 6)
                            open_main_vid()
                            break
                    else:
                        print("closing")
                        player.quit()
                        root.destroy()
                        #command = "python3 add_tag.py"
                        #os.system(command)
                        break


            else:
                print("Card not recognized")
                command = "python3 admin.py " + str(card_data)
                os.system(command)
                open_main_vid()
                read_card()

if __name__ == '__main__':
    Thread(target = open_main_vid).start()
    Thread(target = open_background).start()
    Thread(target = read_card).start()