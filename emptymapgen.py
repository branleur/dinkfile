#Consider this released into the public domain
#Requires Python 3.5 or whatever to run
import struct
import array
import os.path
from sys import exit

def main():
    #First make a dink.dat file that has all the screens activated
    #But check to see if we're going to overwrite something
    if os.path.exists("dink.dat"):
        print("Oh no there's a dink.dat file present! Please move/delete the old one")
        exit()
    else:
        with open("DINK.DAT", "wb") as f:
            #Start with writing the name
            f.write(struct.pack("<24s", b"Smallwood"))
            #Then we need the screens
            #They must all be activated
            screen = array.array('i')
            for i in range(1,768):
                screen.append(i)
            f.write(screen)
            #music and other crap can all be blank
            #You could do some cool stuff with changing this though
            f.write(struct.pack("<3076x"))
            f.write(struct.pack("<3076x"))
            f.write(struct.pack("<2240x"))
            #Alright, the above seems to write a proper Dink.dat file
            print("Wrote Dink.dat file")

    
    if os.path.exists("MAP.DAT"):
        print("Oh no there's a Map.dat file present! Please move/delete the old one")
        exit()
    else:
        with open("MAP.DAT", "wb") as f:
            #Map.dat is just a whole bunch of screens 31280 bytes long from memory. An empty map is just a whole ton of zeroes!
            for i in range(768):
                f.write(struct.pack("<31280x"))
        print("Wrote MAP.DAT file")

if __name__ == "__main__":
    main()