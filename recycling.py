from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os
from threading import Thread
import json
from omxplayer.player import OMXPlayer
from pathlib import Path

global deviceValue
#set to "trash", "compost", or "recycle"
deviceValue = "test"

def open_main_vid():
    global player
    player = OMXPlayer('assets/video/wait_' + deviceValue + '.mp4', args='--loop --layer 1')
    sleep(2)
    
#display video after scanning
def open_vid(vid, vid_length):
    player2 = OMXPlayer(vid, args='--layer 2')
    sleep(vid_length)
    player2.quit()
    
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
            
            for i in list_keys:
                if card_data in tag_dictionary[i]["uids"]:
                    print(i)
                    if i != "killtag":
                        if deviceValue == tag_dictionary[i]["category"]:
                            open_vid("assets/video/" + tag_dictionary[i]["category"] + ".mp4", 14 + 2)#lengh of vid + time it takes to start
                            break
                        else:
                            open_vid("assets/video/wrong.mp4", 6 + 2)
                            break
                    else:
                        print("Closing")
                        try:
                            player.quit()
                        except:
                            print("Player not running")
                        try:
                            player2.quit()
                        except:
                            print("Player 2 not running")
                        #command = "python3 add_tag.py"
                        #os.system(command)
                        break

            else:
                print("Card not recognized")
                try:
                    player.quit()
                except:
                    print("Player not running")
                command = "python3 admin.py " + str(card_data)
                os.system(command)
                Thread(target = open_main_vid).start()
                continue
        sleep(1)

if __name__ == '__main__':
    try:
        Thread(target = open_main_vid).start()
        Thread(target = read_card).start()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)