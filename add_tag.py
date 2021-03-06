from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os
import cv2
from threading import Thread
import json
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

jsonFile = open("shared/tagData.json", "r") # Open the JSON file for reading
data = json.load(jsonFile) # Read the JSON into the buffer
jsonFile.close() # Close the JSON file

tag_dictionary = data["tags"]
combo = ""
card_data = ""
val_unassign = ""
list_keys = list(tag_dictionary.keys())


def window():
    master = Tk()

    master.title("Assign Tags")
    master.geometry('400x400')
    master.configure(background = "white");
    
    lbl = Label(master, text="Scan for tags then choose a tag name to assign")
    lbl.grid(column=0, row=0)
    
    

    def assign_card():
        data["tags"][combo.get()]["uids"].append(card_data)
        
        ## Save our changes to JSON file
        jsonFile = open("shared/tagData.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        
        #print(combo.get())
        print(card_data + " assigned to " + combo.get())
        messagebox.showinfo('Success!', "Tag has been assigned to " + combo.get())
        master.destroy()
        window()
    
    def unassign_card():
        data["tags"][val_unassign]["uids"].remove(card_data)
        
        ## Save our changes to JSON file
        jsonFile = open("shared/tagData.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        
        print(card_data + " unassigned from " + val_unassign)
        messagebox.showinfo('Success!', "Tag has been unassigned from " + val_unassign)
        master.destroy()
        window()
        
    def scan_button():
        lbl2.configure(text="Listening for tags...")
        read_card()
        
           
    def read_card():
        master.update_idletasks()
        
        card_detected = False
            
        while card_detected == False:
            
            pn532 = Pn532_i2c()
            pn532.SAMconfigure()
            
            global card_data
            card_data = pn532.read_mifare().get_data().hex()
            
            if card_data != "4b00":
                card_detected = True
                print(card_data)
                
                global combo
                combo = Combobox(master)
                combo['values']= (list_keys)
                combo.current(0) #set the selected item
                combo.grid(column=0, row=3)
                #print(combo.get())
                
                button = Button(master, state=DISABLED, text="Assign Tag", command=assign_card)
                button.grid(column=0, row=4)
                button2 = Button(master, state=DISABLED, text="Unassign Tag", command=unassign_card)
                button2.grid(column=0, row=5)
                
                global val_unassign
                
                for i in list_keys:
                    if card_data in tag_dictionary[i]["uids"]:
                        
                        print("Tag already assigned to " + i)
                        lbl2.configure(text="Tag already assigned to " + i)
                        val_unassign = i
                        combo.grid_forget()
                        #button.grid_forget()
                        button.config(state="disabled")
                        button2.config(state="normal")
                        break
                
#                 if card_data in tag_dictionary["tag1"]:
#                     print("Tag already assigned to card 1")
#                     lbl2.configure(text="Tag already assigned to card 1")
#                     val_unassign = "tag1"
#                     combo.grid_forget()
#                     button2.config(state="normal")
# 
#                 elif card_data in tag_dictionary["tag2"]:
#                     print("Tag already assigned to card 2")
#                     lbl2.configure(text="Tag already assigned to card 2")
#                     val_unassign = "tag2"
#                     combo.grid_forget()
#                     button2.config(state="normal")

                else:
                    print("Tag not currently assigned")
                    lbl2.configure(text="Tag found with UID: " + card_data)
                    button.config(state="normal")
                    button2.config(state="disabled")
                    #button2.grid_forget()
                    
            time.sleep(.1)
    
    scanButton = Button(master, text="Scan for Tags", command=scan_button)
    scanButton.grid(column=0, row=1)
    
    lbl2 = Label(master, text="No tags detected")
    lbl2.grid(column=0, row=2)

    mainloop()
            
window()