"""ddecompress - attempts to decompress .d script files"""
import click
import struct
import os
import glob

@click.command()
@click.argument("path")
def checkpath(path):
    """Checks to see if you've provided a dir or a script path"""
    if os.path.isdir(path):
        os.chdir(path)
        #If you've provided a script collection it will attempt to decompress all of them
        scripts = glob.glob("*.d")
        for i in scripts:
            if os.path.getsize(i) > 0:
                decompress(i)
    else:
        if os.path.getsize(path) > 0:
            decompress(path)
        else:
            click.echo("That file is empty")

def decompress(script):
    with open(script, "rb") as f:
        #Get the amount of pairs
        paircount = ord(f.read(1)) - 128
        print("Paircount is %s" % paircount)
        #Get the pair table (indicating what thing greater than 128 are going to expand into)
        pairs = [struct.unpack("BB", f.read(2)) for i in range(paircount)]
        #The byte number in the text body that corresponds to one of the pairs
        indexes = [i + 128 for i in range(paircount)]
        table = dict(zip(indexes, pairs))
        #Process it
        outfile = scanner(f.read(), table)

        with open(os.path.splitext(script)[0] + ".c", "w") as o:
            click.secho("Writing outfile...", fg="yellow")
            o.write(outfile)

def scanner(text, pairtable):
    """Scans through the text and replaces bytes with appropriate pairs"""
    filetext = list(text)
    #Make it do another pass until it can't find anything
    anotherpass = 1
    #Store pass count for interest
    passes = 0
    while anotherpass == 1:
        anotherpass = 0
        passes += 1
        for count, data in enumerate(filetext):
            if data > 127:
                filetext[count] = pairtable[data][0]
                filetext.insert(count + 1, pairtable[data][1])
                anotherpass = 1

    fileout = [chr(i) for i in filetext]
    print("Did %s passes" % passes)

    return ''.join(fileout)

if __name__ == '__main__':
    checkpath()