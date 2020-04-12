import tkinter as tk
from tkinter import font  as tkfont
import json
import sys
import os
from os import path
from PIL import ImageTk, Image
from apscheduler.scheduler import Scheduler
#from svglib.svglib import svg2rlg
#from reportlab.graphics import renderPDF, renderPM

#load object by running script like ' SCRIPTLOCATION/admin.py "variable" '
if len(sys.argv) == 2:
    objectToRegister = sys.argv[1]
else:
    objectToRegister = "undefined"

#potential items and categories
recycle = ["bottle","soda","box"]
trash = ["lightbulb","bone","skateboard"]
compost = ["apple","banana","eggshell"]

#empty variables to be set by program
selectedCat = ""
selectedItem = ""

timeNum = 10
firstTimeOut = 0

sched = Scheduler()
sched.start()

#the greater window
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #comment out next line to turn off fullscreen
        #self.attributes("-fullscreen", True)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")
    def murder(self):
        os._exit(0)

# option to register
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        def quit():
            global timeNum
            global firstTimeOut
            if firstTimeOut == 0:
                timeNum = timeNum - 1
            closingMsg['text'] = "tool will close in "+str(timeNum)
            if timeNum <= 0:
                controller.murder()
        def printit(self):
            global timeNum
            sched.add_interval_job(quit, seconds = 1)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        load = Image.open("temp.gif")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(image=render)
        img.image = render
        #img.pack()
        lbl = tk.Label(self, text="item unidentified", font=("Arial Bold", 50))
        lbl.pack()
        btn = tk.Button(self, text="Register",font=("Arial Bold", 50), bg="white", fg="blue",command=lambda: controller.show_frame("PageOne"))
        btn.pack()
        closingMsg = tk.Label(self, text="tool will close in 10", font=("Arial Bold", 30))
        closingMsg.pack()
        printit(self)

#choose category
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        def nextPage(self,cat):
            global selectedCat 
            selectedCat = cat
            self.controller.show_frame("PageTwo")
        tk.Frame.__init__(self, parent)
        self.update()
        self.controller = controller
        label = tk.Label(self, text="Object Category:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        #recycleDraw = svg2rlg("Icons/recycle.svg")
        #renderPM.drawToFile(recycleDraw, "recyc.png", fmt="PNG")
        recycleImg = ImageTk.PhotoImage(Image.open("assets/images/recyc.png"))
        button = tk.Button(self, image=recycleImg, text="Recycle", command=lambda: nextPage(self,'recycle'))
        button.photo = recycleImg
        button.pack(side=tk.LEFT, expand=1, fill=tk.X)

        #trashDraw = svg2rlg("Icons/trash.svg")
        #renderPM.drawToFile(trashDraw, "trash.png", fmt="PNG")
        trashImg = ImageTk.PhotoImage(Image.open("assets/images/trash.png"))
        button2 = tk.Button(self, image=trashImg, text="Trash", command=lambda:nextPage(self,'trash'))
        button2.photo = trashImg
        button2.pack(side=tk.LEFT, expand=1, fill=tk.X)

        #compDraw = svg2rlg("Icons/compost.svg")
        #renderPM.drawToFile(compDraw, "comp.png", fmt="PNG")
        compostImg = ImageTk.PhotoImage(Image.open("assets/images/comp.png"))
        button3 = tk.Button(self, image=compostImg, text="Compost", command=lambda:nextPage(self,'compost'))
        button3.photo = compostImg
        button3.pack(side=tk.LEFT, expand=1, fill=tk.X) 
          
        self.bind("<<ShowFrame>>", self.on_show_frame)
    def on_show_frame(self,event): 
        global firstTimeOut
        firstTimeOut = 1

#choose object
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        def on_show_frame(self):
            global selectedCat
            global recycle
            global trash
            global compost
            if selectedCat == 'recycle':
                currArray = recycle
            elif selectedCat == 'trash':
                currArray = trash
            elif selectedCat == 'compost':
                currArray = compost
            for index, x in enumerate(currArray):
                buttonArray[index]['text'] = x
                #compDraw = svg2rlg("Icons/"+x+".svg")
                #renderPM.drawToFile(compDraw, x+".png", fmt="PNG")
                recycleImg = ImageTk.PhotoImage(Image.open("assets/images/" + x + ".png"))
                buttonArray[index]['image'] = recycleImg
                buttonArray[index].photo = recycleImg
            label['text'] = ("which",selectedCat,"object?")
        def saveObj(self,x):
            #load info we're using
            global objectToRegister
            typeOfItem = buttonArray[x]['text']

            #checks to see if json exists. loads if it does, creates if it doesn't.
            if path.exists("shared/tagData.json"):
                with open('shared/tagData.json') as json_file:
                    data = json.load(json_file)
            else:
                data = {}
                data['tags'] = []

            #adds data in local json info
            data['tags'][typeOfItem]['uids'].append(objectToRegister)

            #saves json file
            with open('shared/tagData.json', 'w') as outfile:
                json.dump(data, outfile)

            #loads next page
            self.controller.show_frame("PageThree")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="wild", font=self.controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",command=lambda:saveObj(self,0))
        button.pack(side=tk.LEFT, expand=1, fill=tk.X)
        button2 = tk.Button(self, text="Go to the start page",command=lambda:saveObj(self,1))
        button2.pack(side=tk.LEFT, expand=1, fill=tk.X)
        button3 = tk.Button(self, text="Go to the start page",command=lambda:saveObj(self,2))
        button3.pack(side=tk.LEFT, expand=1, fill=tk.X)
        buttonArray = [button,button2,button3]
        self.bind("<<ShowFrame>>", on_show_frame)

#success screen
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        def on_show_frame(self):
            global timeNum
            timeNum = 3
            printit(self)
        def quit():
            global timeNum
            global firstTimeOut
            timeNum = timeNum - 1
            closingMsg['text'] = "tool will close in "+str(timeNum)
            if timeNum <= 0:
                controller.murder()
        def printit(self):
            global timeNum
            sched.add_interval_job(quit, seconds = 1)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Saved!", font=self.controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        closingMsg = tk.Label(self, text="tool will close in 3", font=("Arial Bold", 30))
        closingMsg.pack()
        self.bind("<<ShowFrame>>", on_show_frame)
        
#checks if json exists, if it doesn't, creates it.
if path.exists("data.json"):
    with open('data.json') as json_file:
        data = json.load(json_file)
else:
    data = {}
    data['tags'] = []

#initiatory loop
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()