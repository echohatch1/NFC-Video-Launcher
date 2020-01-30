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

jsonFile = open("tagData.json", "r") # Open the JSON file for reading
data = json.load(jsonFile) # Read the JSON into the buffer
jsonFile.close() # Close the JSON file

tag_dictionary = data["tags"][0]
combo = ""
card_data = ""
val_unassign = ""

def window():
    master = Tk()

    master.title("Assign Tags")
    master.geometry('400x400')
    master.configure(background = "white");
    
    lbl = Label(master, text="Choose a tag name to assign and then scan for a tag")
    lbl.grid(column=0, row=0)
    
    global combo
    combo = Combobox(master)
    combo['values']= ("tag1", "tag2")
    combo.current(0) #set the selected item
    combo.grid(column=0, row=1)
    #print(combo.get())

    def assign_card():
        data["tags"][0][combo.get()].append(card_data)
        
        ## Save our changes to JSON file
        jsonFile = open("tagData.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        
        #print(combo.get())
        print(card_data + " assigned to " + combo.get())
        messagebox.showinfo('Success!', "Tag has been assigned")
    
    def unassign_card():
        data["tags"][0][val_unassign].remove(card_data)
        
        ## Save our changes to JSON file
        jsonFile = open("tagData.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        
        print(card_data + " unassigned from " + val_unassign)
        messagebox.showinfo('Success!', "Tag has been unassigned")
           
    def read_card():

        card_detected = False
            
        while card_detected == False:
            pn532 = Pn532_i2c()
            pn532.SAMconfigure()
            
            global card_data
            card_data = pn532.read_mifare().get_data().hex()
            
            if card_data != "4b00":
                card_detected = True
                print(card_data)
                button = Button(master, state=DISABLED, text="Assign Tag", command=assign_card)
                button.grid(column=0, row=4)
                button2 = Button(master, state=DISABLED, text="Unassign Tag", command=unassign_card)
                button2.grid(column=0, row=5)
                
                global val_unassign
                
                if card_data in tag_dictionary["tag1"]:
                    print("Tag already assigned to card 1")
                    lbl2.configure(text="Tag already assigned to card 1")
                    val_unassign = "tag1"
                    button2.config(state="normal")

                elif card_data in tag_dictionary["tag2"]:
                    print("Tag already assigned to card 2")
                    lbl2.configure(text="Tag already assigned to card 2")
                    val_unassign = "tag2"
                    button2.config(state="normal")

                else:
                    print("Tag not currently assigned")
                    lbl2.configure(text="Tag found with UID: " + card_data)
                    button.config(state="normal")
    
    scanButton = Button(master, text="Scan for Tags", command=read_card)
    scanButton.grid(column=0, row=2)
    
    lbl2 = Label(master, text="No tags detected")
    lbl2.grid(column=0, row=3)

    mainloop()
            
window()