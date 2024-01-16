from tkinter import *
from PIL import Image, ImageTk
import pathlib
from sys import argv, exit
import dfile.harddat

#Specify the tile path on the command line
#And a path to Hard.dat
tilpath = pathlib.Path(argv[1])
hpath = pathlib.Path(argv[2])

def drawnum():
    #Draw the numbers on the canvas when the box is ticked
    canv.delete("texts")
    if CheckVar1.get() == 1:
        count = 0
        for y in range(0, 400, 50):
            for x in range(0, 600, 50):
                tilnum = (int(S1.get()) -1) * 128 + count
                canv.create_text(x + 20, y + 20, text=str(tilnum), tag="texts", fill="red")
                if CheckVar3.get() == 1:
                    #Draw the hard shit here instead. Get the tile number being drawn and see if it's in the index
                    if hindex[tilnum] > 0:
                        canv.create_image(x, y, anchor=NW, image=baginas[hindex[tilnum]], tag="hards")
                count += 1
            #count += 1    
    if CheckVar1.get() == 0:
        canv.delete("texts")
    if CheckVar3.get() == 0:
        canv.delete("hards")

def drawgrid():
    #Draw gridlines on the canvas
    if CheckVar2.get() == 1:
        for x in range(50, 600, 50):
            canv.create_line(x, 0, x, 600, fill="magenta", tag="crap")

            for y in range(50, 400, 50):
                canv.create_line(0, y, 600, y, fill="magenta", tag="crap")
    else:
        #delete the gridlines as per the tag
        canv.delete("crap")

def spinny(*args):
    #Activate the spinner box to change the tile screen
    #print(S1.get())
    canv.delete("tiley")
    canv.create_image(0,0, anchor=NW, image= benises[int(S1.get()) - 1], tag="tiley")
    canv["bg"] = "black"
    drawgrid()
    drawnum()

if tilpath.exists():
    #The inputted path is real
    tiles = tilpath.glob("[Tt][Ss]*.bmp")
    tilscrs = []
    for i in tiles:
        tilscrs.append(Image.open(i))

if hpath.exists():
    #Get Hard.dat
    htiles = dfile.harddat.openhdat(hpath, nukefifty=True)
    hindex = dfile.harddat.opentindex(hpath)
    tils = []
    #Convert the hard tiles into graphics with transparency
    for num, i in enumerate(htiles):
        tile = Image.new("RGBA", (50,50), color=(255,255,255,0))
        x = 0
        y = 0
        for count, thing in enumerate(i):
            if thing == 1:
                col = (255,255,0,200)
            elif thing == 2:
                col = (0,0,255,200)
            else:
                col = (255,255,255,0)
            if y < 50 and x < 50:
                tile.putpixel((x,y), col)
            #print(x,y)
            y += 1      
            if y == 50:
                y = 0
                x += 1
        #tile.save("nigger" + str(num) + ".png")
        tils.append(tile)
    

    
    #GUI shit
    master = Tk()
    master.title("Dink Tile Viewer")
    master.resizable(False, False)
    Spinvar = StringVar()
    S1 = Spinbox(master, from_=1, to=41, textvariable="Spinvar", command=spinny)
    S1.bind("<Return>", spinny)
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    CheckVar3 = IntVar()
    C1 = Checkbutton(master, text= "Tile Numbers", variable = CheckVar1, onvalue = 1, offvalue = 0, height=1, width =10, command=drawnum)
    C2 = Checkbutton(master, text= "Gridlines", variable = CheckVar2, onvalue = 1, offvalue = 0, height = 1, width = 10, command=drawgrid)
    C3 = Checkbutton(master, text="Hard.dat Squares (Make sure numbers is on)", variable=CheckVar3, onvalue = 1, offvalue = 0, height = 1, width = 35, command = drawnum)
    canv = Canvas(master, width=600, height=400, bg="blue")
    

    canv.pack(side=BOTTOM)
    S1.pack(side=LEFT)
    C1.pack(side=RIGHT)
    C2.pack(side=LEFT)
    C3.pack(side=LEFT)

    #seems this needs to be done after TK has initialised
    #It converts them to a Tkimage so that they may be displayed on the canvas
    benises = []
    baginas = []
    for i in tilscrs:
        benises.append(ImageTk.PhotoImage(i))
    canv.create_image(0,0, anchor=NW, image= benises[0], tag="tiley")

    for i in tils:
        baginas.append(ImageTk.PhotoImage(i))
    
    

    mainloop()