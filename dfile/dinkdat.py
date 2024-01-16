"""This handles the saving and loading of dink.dat files"""
import struct
import array
import json
from os.path import join

def readindex(file):
    '''Opens a Dink.dat file and returns its data
    >>> index = readindex("tests\dink.dat")
    >>> index['screenno'][0]
    1
    '''
    index = {}
    with open(file, "rb") as f:
        #Skip the name
        #The last four bytes are the first index of screenno actually
        f.read(24)
        #Dink.dat is a very simple file that stores only the screen index for map.dat
        #Along with the MIDI number of the screens and their "indoor" status
        index['screenno'] = list(struct.unpack('<768i', f.read(4 * 768)))
        f.read(4)
        index['midi'] = list(struct.unpack('<768i', f.read(4 * 768)))
        f.read(4)
        index['indoor'] = list(struct.unpack('<768i', f.read(4 * 768)))

    return index


def save(index, path):
    '''Saves an index of Dink screens into a data file into a specified path'''
    with open(join(path, "DINK.DAT"), "wb") as f:
        #Should do checks for proper data sizes in future maybe
        name = struct.pack('<24s', b'Smallwood')
        screenno = array.array('i')
        midi = array.array('i')
        indoor = array.array('i')
        index['screenno'].append(0)
        index['midi'].append(0)
        screenno.fromlist(index['screenno'])
        midi.fromlist(index['midi'])
        indoor.fromlist(index['indoor'])  
        padding = struct.pack('<2240x')
        dinkdat = name + bytes(screenno + midi + indoor) + padding
        f.write(dinkdat)

def savejson(index, path):
    '''Exports a Dink index into a JSON file'''
    with open(join(path, 'index.json'), 'w') as f:
        json.dump(index, f, indent=4)

def newindex():
    '''Returns an empty map index'''
    index = {}

    for i in ('screenno', 'midi', 'indoor'):
        index[i] = [0] * 768
    return index

if __name__ == "__main__":
    import doctest
    doctest.testmod()