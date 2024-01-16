Dinkfile - A collection of utilities for Dink Smallwood
======================================================

Herein lies a collection of possibly useful little programs for dealing with Dink Smallwood data files. Included is a map editor and a few other things.
If you're a cool hacker you could use the modules to create your own data file editor or even a random map generator or something or otherwise use it in the traditional Dink style as an example of what you shouldn't do when designing something.

Requirements
-------------

You'll need a Python 3 interpreter in your path. I used Python 3.5 although most versions of 3 should work as long as they have pathlib.
At the moment it requires Bottle, Click, Pillow, and pyglet. Use Pip to install them (pip install bottle etc).
Certain files also require pygame and pygcurse.

File description
----------------

+ dfarctar.py - A decompressor for broken tar files created with early releases of DFarc. Takes one argument, the tar file within the bz2. Is written to be Windows-only but could be easily modified to work on other systems.

+ emptymapgen.py - Generates a dink.dat and map.dat of 768 screens all completely empty.

+ mapstats.py - Analyser for dink maps. It tells you how many map screens you have and little else. Run it with a MAP.DAT file on the end if you're really interested.

+ hardboxreplace.py - Replaces the depth dot values for SET_SPRITE_INFO lines in dink.ini. The first argument is the path to dink.ini, the second is the sequence, and the third and fourth are your new depth dot values.

+ hardfix.py - Repairs broken hard.dat files mangled by FreeDinkEdit that are lacking the required amount of indices. Requires a path to hard.dat.

+ photohard.py - Hard.dat editing the easy way! Supply a path to hard.dat, your masking image PNG, and your tilescreen number on the command line and photohard will automatically edit hard.dat with the contents of your masking image for your new tile screen. No longer will you have to toil with stamping individual squares. Water/low hard must be drawn in pure blue, and normal in red for it to be picked up. Currently is very dumb and wasteful due to not scanning through existing tiles but might be good for small dmods.

+ htileview.py - Provides a graphical representation of the collision squares in HARD.DAT. This requires pygame and pygcurse. You can download pygcurse from Al Sweigart's site and drop it next to this file for it to work. 
	- Feed it a hard.dat file and it should hopefully give you an idea of what the file contains on each square. Use the left and right keys to select the appropriate square.
	- Pressing left at the beginning will take you to the last square (800). It's very slow and you can't edit anything. Deal with it.

+ tileviewtk.py - This is similar to the above except it uses Tkinter in order to show the map tiles with their numbers along with the hard.dat tiles that apply to them. It takes two arguments with the first being a path to your TILES collection with the other being your corresponding HARD.DAT file.

+ dinkinichk.py - This is an attempt to make something that looks for problems with dink.ini. So far it can find certain problems but doesn't fix them. Obviously feed it a dink.ini file for it to work.

+ dmodpacker.py - If you want to distribute a mod for Dink that you've made, you'll need to archive it so that files don't go missing. The *.dmod files that are used by DFarc are actually just tar.bz2 files renamed (except for early versions of DFarc that apparently didn't use the tar library). Deletes useless files such as debug.txt and skeleton.txt before packing and gives some warnings if there are files missing.

+ ddecompress.py - A decompresser for byte-pair encoded .d files. run `python ddecompress.py myscript.d` to get a decompressed outfile. Will also batch convert a provided dirpath.

+ dinkiniview.py - Allows you to view the sequence collections in dink.ini. Requires pyglet to run. run it as `python dinkiniview.py dink.ini dinkdatapath`

+ ffunpack.py - Opens dir.ff Fastfile packs. Specify the dir.ff path for it to open and it will dump out all the bmps (and other files) within it. Doesn't work properly with newer .ff files like Mystery Island's though which bundle everything up into one file. Probably won't work at all.

+ map2script.py - This takes a Dink map screen and turns it into a script consisting of a bunch of `create_sprite` DinkC commands and `map_tile` for the tiles etc. It takes a path containing map.dat and dink.dat with the other argument being the outputted dinkc file's name. The last argument is the screen number in question to convert. Run it with `python3 map2script.py map.dat outscript.c 45` to make a script out of screen 45.

+ tileview.py - Shows you the numbers of the tiles on each tile screen. Feed it your tiles path to open them. Currently doesn't work with dmods, only main game.

+ hard2gif.py - Turns a HARD.DAT collision data file into both a paletted gif and a JSON file containing the tile to hard.dat index.

+ shareware.py - Homage to the DOOM shareware exit screen. Requires pygame and pygcurse.