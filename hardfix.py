from sys import argv
from os.path import isdir, getsize
from os import truncate
from pathlib import Path

def fixhard(hdatfilepath):
    if getsize(hdatfilepath) < 2107392:
        print("Hard.dat found with missing indices... Fixing...")
        #Let's bump it up to the nominal size with 8000 slots just in case
        truncate(hdatfilepath, 2118400)
    else:
        print("Hard.dat is fine. Skipping...")

def main(argv):
    if len(argv) < 2:
        print("Please specify a HARD.DAT file or a dirpath as an argument")
    else:
        if isdir(argv[1]):
            print("Scanning through folders for broken HARD.DATs")
            p = Path(argv[1])
            for i in p.rglob("hard.dat"):
                print(i)
                fixhard(i)
        else:
            #We have a single file specified on the command line. Perform input testing...
            if not "hard.dat" in argv[1]:
                print("This is not a hard.dat file!")
            else:
                fixhard(argv[1])

if __name__ == "__main__":
    main(argv)