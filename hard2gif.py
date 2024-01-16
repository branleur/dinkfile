"""Hard2bmp - converts a Dink hard.dat file into a standard windows bitmap file along with the indices into JSON"""
#Actually it makes GIF files

import dfile.harddat
from PIL import Image
import click
import json
import os.path

@click.command()
@click.argument("harddat")
#@click.option("-col", default=1, help="The amount of columns in the bmp file")
def conv(harddat):
    """Converts a hard.dat file to a BMP and json file"""
    if not os.path.exists(harddat):
        click.echo("File not found. Check the path and try again")
        return
    else:
        if os.path.basename(harddat).upper().startswith("HARD"):
            print("Found hard.dat")
            hdat = dfile.harddat.openhdat(harddat)
            tindex = dfile.harddat.opentindex(harddat)

            himg = Image.new("P", (50, 51*800), 0)
            #Palette is 0=white, 1= yellow, 2= blue, 3= red, 4= green
            pal = [255,255,255, 255,255,0, 0,0,255, 255,0,0, 0,255,0]
            himg.putpalette(pal)
            x = 0
            y = 0
            for i in hdat:
                himg.paste(mkhimg(i, pal), (x, y))
                y += 51

            himg.save("hard.gif")
            
            with open("hard.json", "w") as f:
                json.dump(tindex, f,indent=4)

def mkhimg(til, pal):
    """Takes collision tile data and turns it into a pic"""
    tile = Image.new("P", (51,50), 0)
    tile.putpalette(pal)
    tile.putdata(til)
    #For some reason this shit is backwards in PIL
    out = tile.transpose(Image.ROTATE_270)
    out = out.transpose(Image.FLIP_LEFT_RIGHT)
    return out



if __name__ == '__main__':
    conv()