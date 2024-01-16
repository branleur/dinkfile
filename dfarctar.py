#dfarctar.py - Extracting the broken TAR files from original DFarc
#windows won't allow a folder with the same name as a file...
import struct
import click
import pathlib
import arrow
import os.path
from win32_setctime import setctime

@click.command()
@click.argument("tar")
def extract(tar):
    with open(tar, "rb") as f:
        while True:
            click.secho("Even if it chucks an error it should work", fg="blue")
            #Load the filename first. I should really have done this differently. Oh well.
            fname = struct.unpack("100s", f.read(100))[0].decode("oem").strip("\x00")
            click.secho("Filename is %s" % fname, fg="green")
            #Skip the mode and shit
            f.read(24)
            #Size in octal
            size = int(struct.unpack("12s", f.read(12))[0].decode("oem").strip("\x00"), 8)
            print(size)
            #Date
            date = int(struct.unpack("12s", f.read(12))[0].decode("oem").strip("\x00"), 8)
            print(arrow.get(date))
            checksum = struct.unpack("8s", f.read(8))[0].decode("oem").strip("\x00")
            #Typeflag and other crap
            f.read(356)
            #Read the file
            p = pathlib.Path(fname)
            if not os.path.exists(p.parent):
                p.parent.mkdir(parents=True)
            with open(p, "wb") as o:
                o.write(f.read(size))
            #Add the proper time
            setctime(p, date, follow_symlinks=True)    
            #Get the next file by rounding up to 512 bytes
            if size % 512 != 0:
                f.read(512 - (size % 512))

    


if __name__ == "__main__":
    extract()