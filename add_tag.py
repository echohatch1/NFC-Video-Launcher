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

def window():
    master = Tk()

    master.title("Welcome to TutorialsPoint")
    master.geometry('400x400')
    master.configure(background = "white");
    
    lbl = Label(master, text="Choose a tag name to assign and then scan for a tag")
    lbl.grid(column=0, row=0)

    combo = Combobox(master)
    combo['values']= ("tag1", "tag2")
    combo.current(0) #set the selected item
    combo.grid(column=0, row=1)

    def ok():
        print ("tag assigned")
        messagebox.showinfo('Success!', "Tag has been assigned")
           
    def read_card():
        data = json.load(open('tagData.json'))
        card_detected = False
            
        while card_detected == False:
            pn532 = Pn532_i2c()
            pn532.SAMconfigure()

            card_data = pn532.read_mifare().get_data().hex()
            
            if card_data != "4b00":
                card_detected = True
                print(card_data)
                lbl2.configure(text="Tag found with UID: " + card_data)
                button = Button(master, text="Assign Tag", command=ok)
                button.grid(column=0, row=4)
    
    scanButton = Button(master, text="Scan for Tags", command=read_card)
    scanButton.grid(column=0, row=2)
    
    lbl2 = Label(master, text="No tags detected")
    lbl2.grid(column=0, row=3)

    mainloop()
            
window()