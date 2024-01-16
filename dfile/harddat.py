"""harddat.py allows you to load collision data from Dink Smallwood 'hard.dat' files."""
import array
import struct

def openhdat(filename, nukefifty=False):
    """This just makes a list of size 800 with each index being a collision tile consisting of a stream of ones or twos etc
    For example to get the value of the pixel at the beginning of square 4 you would go ctile[4][0] and each tile is 51x51 pixels big"""
    ctiles = []
    with open(filename, "rb") as f:
        for i in range(800):
            square = f.read(2550)
            #Blank data of 58 bytes at the end of each square I believe
            #The bytes are actually part of the "hold" and "used" data that was never used
            f.read(58)
            arr = array.array("B", square)
            til = arr.tolist()
            if nukefifty == True:
                for i in range(50,2550, 50):
                    til.pop(i)

            ctiles.append(til)
            

    return ctiles

def opentindex(filename):
    """This opens the tile index that is part of hard.dat. The individual tiles from the graphics in TILES/ are given their default collision stats according to what's in here"""
    #Do this later or merge it into the above
    tindex = []
    with open(filename, "rb") as f:
        f.seek(2086400)
        #WC claims there are 3936 values in this table but I think there may be 5248 or so. Dinkvar.h may indicate 8000. 
        #The filesize of the original hard.dat indicates 5248 as per Magicman's calcs
        #There's some weird data in the original release file such as filepaths and other stuff
        #Redink's Hard.dat rewrite has all 8000 spaces
        #Each one is 4 bytes
        tindex = list(struct.unpack("<5248i", f.read()[:20992]))
        return tindex

def savehard(filename, squares, tindex):
    """Takes a filename and a list of 800 squares and a tile index of 5248 values and saves it to filename"""
    #First check that the things are of the proper length
    #And that all the index values are 800 or less
    if len(squares) != 800:
        print("There are not enough squares")
        raise IOError

    if len(tindex) < 5248:
        print("There are not enough indices")
        raise IOError
        
    with open(filename, "wb") as f:
        for i in squares:
            #Write the square
            f.write(struct.pack("<58x"))