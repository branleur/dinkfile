#Performs screen-related stuff involving both map.dat and dink.dat data but not the files themselves
#Probably should have made a proper MVC framework for this sort of crap
import logging
import dfile.mapdat

def new(index, mapping, number, copy=False, MIDI=0, script='', indoor=0):
    """Creates a new screen of a particular number"""
    if index['screenno'][number -1] == 0:
        if number == 1:
            mapno = 1
        else:
            mapno = max(index['screenno'][0:number-1]) + 1

        index['screenno'][number-1] = mapno
        index['midi'][number-1] = MIDI
        index['indoor'][number-1] = indoor

        if copy and (0 < int(copy) <= 768) and (index['screnno'][int(copy)] > 0):
            logging.info("Copying a screen")
            newscr = mapping[index['screnno'][copy-1]]
        else:
            newscr = {'tileno': [0] * (8 * 12), 'alt_hard': [0] * (8 * 12), 'sprites': [0] * 200, 'script': script.encode()}

        for i in range(100):
            newscr['sprites'][i] = {}
            for j in dfile.mapdat.spriteattr:
                if j in ('script', 'hit', 'die', 'talk'):
                    newscr['sprites'][i][j] = ""
                else:
                    newscr['sprites'][i][j] = 0

        mapping.insert(mapno -1, newscr)
        for i in range(number, 768):
            #I could probably rewrite this using list comprehension
            if index['screenno'][i] > 0:
                index['screenno'][i] += 1

        return index, mapping
    
    else:
        logging.warning("Screen %s already exists" % number)
        return False

def delete(index, mapping, number):
    """Delete a screen of a particular number"""
    screen = index['screenno'][number - 1]
    logging.info("Deleting screen")
    if screen != 0:
        mapping.pop(screen -1)
        index['screenno'][number -1] = 0
        for i in range(number, 768):
            if index['screenno'][i] > 0:
                index['screenno'][i] -= 1

        return index, mapping

    else:
        logging.info("Screen doesnt exist and therefore was not deleted")
        return False

def edit(map, index, screen):
    """Edits a single map screen"""
    #Presumably this receives a map screen and plops it into the map data or something. Not sure yet.
    pass

def move(source, dest, index, map):
    """Moves a map screen from one index to another"""
    pass