# photohard - a thing for making hard.dat tiles in photoshop
from PIL import Image
from sys import argv
import dfile.harddat
from pathlib import Path
#import xdialog
import struct
import array
import PySimpleGUI as sg

def mergetile(imdata):
    #Make a new tile with the data we've supplied
    tile = []
    for y in range(50):
        for x in range(50):
            if imdata[y, x] == (0,0,255,255):
                #Water/low - blue
                tile.append(1)
            elif imdata[y, x] == (255,0,0,255):
                #Normal collision - red in colour picker
                tile.append(2)
            elif imdata[y, x] == (255,255,255,0):
                #Transparent - no collision
                tile.append(0)
            else:
                #Just assume it's transparent otherwise
                tile.append(0)
        #blank row
        tile.append(0)
    return tile

def getempt(tilist):
    for count,thing in enumerate(tilist):
        #Tile zero should always be blank, otherwise return the empty tile
        if max(thing) == 0 and count !=0:
            return count

def getdup(htile, tilist):
    #Search through the tile squares to see if there's an existing match
    pass

#Starts here
if len(argv) < 2:
    print("Please specify your hard.dat, masking PNG, and tile screen number on the command line")
    # hdat = xdialog.open_file("Select your Hard.dat", filetypes=[("Dink Collision Data", "hard.dat")], multiple=False)
    # tiles = dfile.harddat.openhdat(hdat)
    # tindex = dfile.harddat.openindex(hdat)
    # colmask = xdialog.open_file("Select your masking PNG", filetypes=[("Portable Network Graphics", "*.png")], multiple=False)
    # # All this just to get the number
    # layout = [[sg.Text("Please enter your intended tile screen number"), sg.InputText()],
    #             [sg.Button('Ok'), sg.Button('Cancel')]]
    # window = sg.Window("Photohard", layout)
    # while True:
    #     event, values = window.read()
    #     if event == sg.WIN_CLOSED or event == 'Cancel':
    #         break
    #     tsnum = int(values[0])
    # window.close()
else:
    #hard dat, collision image, tile screen number
    tiles = dfile.harddat.openhdat(argv[1], nukefifty=False)
    tindex = dfile.harddat.opentindex(argv[1])
    tsnum = int(argv[3])
    colmask = argv[2]
    if 0 < tsnum > 41:
        print("Invalid tile screen")

#Load our collision image
with Image.open(colmask) as im:
    #px = im.load()
    ecks, why = im.size
    #Make it bigger if it's smaller than specified bounds
    if im.size[0] < 600 and im.size[1] < 450:
        ig = Image.new("RGBA",(600,450),(255,255,255,0))
        ig.paste(im,(0,0,ecks,why))
        im = ig
    tile = 128 * (tsnum - 1)
    #Get our tile indices based upon the tilescreen number. Could be changed to do 128 tiles per screen if necessary
    for y in range(0,450,50):
        for x in range(0,600,50):
            # Left, Upper, Right, Lower. Origin top left
            r = x + 50
            #Lower
            l = y + 50
            sq = im.crop((x,y,r,l))
            #sq.save(str(tile + 1) + ".png", "PNG")
            #Check if there's actually image data in it (alpha band)
            if max(list(sq.getdata(3))) != 0:
                #Get an empty tile and write to it and update the index
                tilno = getempt(tiles)
                tiles[tilno] = mergetile(sq.load())
                tindex[tile] = tilno
            else:
                #Otherwise make sure it's assigned blank (tile zero)
                tindex[tile] = 0
            tile +=1
            print(".", end=".")

with open("harddat.dat", "wb") as o:
    for count,thing in enumerate(tiles):
        t = array.array("B")
        t.fromlist(thing)
        o.write(t)
        o.write(struct.pack("58x"))
    ti = array.array("i")
    ti.fromlist(tindex)
    o.write(ti)
    print("\nWrote harddat.dat\n")