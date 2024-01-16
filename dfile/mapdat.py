"""This handles the loading and saving of MAP.DAT files."""
import struct
import os
import logging
import json

spriteattr = ('x','y','seq','frame','type','size','active','rotation','special','brain','script','hit','die','talk','speed','basewalk','baseidle','baseattack','basehit','delay','depth','hardness','trimleft','trimtop','trimright','trimbottom','warpstatus','warpscreen','warpx','warpy','touchseq','basedeath','gold','hitpoints','strength','defense','experience','sound','vision','nohit','touchdamage','junk')

def readmap(file):
    """Opens a specified MAP.DAT file and returns a dict containing its contents
    >>> map = readmap("tests/map.dat")
    >>> len(map)
    18
    """
    #Probably should rewrite that as "map" is a reserved keyword
    msize = os.stat(file).st_size
    logging.info("Map.dat file is %s bytes long" % msize)
    if msize % 31280 != 0:
        #This won't open quest for dorinthia or assweasel's dmods where he uses that map to base his stuff upon
        print("File is not a valid map")
        raise IOError
    else:
        scrcount = msize / 31280
        if scrcount > 768:
            logging.warning("Lol wtf is with this big map?")

    maps = []
    with open(file, 'rb') as f:
        for i in range(int(scrcount)):
            screen = {}
            mapscreen = f.read(31280)
            for i in ('tileno', 'sprites', 'alt_hard'):
                screen[i] = []
            
            for j in range(96):
                screen['tileno'].append(struct.unpack('<i', mapscreen[(80*j)+20: (80*j)+24])[0])
                screen['alt_hard'].append(struct.unpack('<i', mapscreen[(80*j)+28: (80*j)+32])[0])

            for i in range(100):
                screen['sprites'].append(dict(zip(spriteattr, struct.unpack('<10i13s13s13s13s29i', mapscreen[(220 * i) + 8240:(220 * i) + 8448]))))
                for q in ('script', 'hit', 'die', 'talk'):
                    screen['sprites'][i][q] = screen['sprites'][i][q].decode(errors="replace").strip("\x00")


            screen['script'] = struct.unpack('<20s', mapscreen[30240:30260])[0].decode(errors="replace").strip("\x00")
            maps.append(screen)
    return maps

def newmap():
    """Returns an empty map"""
    #yeah
    maps = []

    return maps

def save(mapping, path):
    """Saves a map into MAP.DAT"""
    with open(os.path.join(path, 'map.dat'), 'wb') as f:
        #Should probably use a better name than 'thing'
        for count,thing in enumerate(mapping):
            screen = struct.pack('<20x')
            for i in range(8 * 12):
                screen += struct.pack('<i', int(thing['tileno'][i]))
                #I am not using the starts at one scheme here so this 4 byte thing is necessary
                screen += struct.pack('<4x')
                screen += struct.pack('<i', int(thing['alt_hard'][i]))
                screen += struct.pack('<68x')
            sprites = struct.pack('<540x')

            for i in range(100):
                for j in (spriteattr):
                    if j in ('script','hit','die','talk'):
                        sprites += struct.pack('<13s', thing['sprites'][i][j].encode())
                    elif j == "junk":
                        sprites += struct.pack('<20x')
                    else:    
                        sprites += struct.pack('<i', int(thing['sprites'][i][j]))
            sprites += struct.pack('<20s', thing['script'].encode())
            screen += sprites + struct.pack('<1020x')
            f.write(screen)

def savejson(maps, path):
    """Exports the map to JSON"""
    #Make it so that it cleans up the map data by removing empty stuff
    with open(os.path.join(path, 'map.json'), 'w') as f:
        json.dump(maps, f, indent=4)

if __name__ == "__main__":
    import doctest
    doctest.testmod()