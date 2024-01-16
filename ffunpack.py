"""FFunpack for extracting ff files"""
#TODO: Make it skip files with a zero offset
import struct
import click
import pathlib
from os import chdir

@click.command()
@click.argument("dirff")
@click.argument("outpath", default=".")
def extract(file, outpath):
    """Attempts to get BMP files out of an ff file"""
    p = pathlib.Path()
    ffs = p.rglob("dir.ff")
    files = []
    offsets = []
    for i in ffs:
        with open(i, "rb") as f:
            #The first integer (four bytes) of the file shows how many file entries are in it plus one
            counter = struct.unpack("i", f.read(4))[0] - 1
            print("There are %s entries in this file" % counter)
            #The next integer shows the starting offset of the first file
            for i in range(counter):
                offset = struct.unpack("i", f.read(4))[0]
                offsets.append(offset)
                fname = struct.unpack("13s", f.read(13))[0].decode().strip("\x00")
                files.append(fname)
            end = struct.unpack("i", f.read(4))[0] - 1

            for count, filename in enumerate(files):
                with open(filename, "wb") as o:
                    f.seek(offsets[count])
                    if count + 1 == len(files):
                        #This is the last one
                        entry = end
                        
                    else:
                        entry = offsets[count] - 1
                    bmp = f.read(entry)
                    if outpath != ".":
                        chdir(outpath)
                    o.write(bmp)
                    click.secho("Wrote %s" % (filename), fg="yellow")
            i.unlink()


if __name__ == '__main__':
    extract()