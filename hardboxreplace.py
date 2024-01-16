from pathlib import Path
from sys import argv, exit
#Overwrite a SET_SPRITE_INFO line with new hardbox
#SET_SPRITE_INFO seq, frame, depth dot(x,y), hardbox(rect)
#First arg is filename, second is seq, third and fourth are depth dot numbers being changed
if len(argv) < 4:
    print("First arg is dink.ini path, second is seq, third and fourth are your new depth dot")
    exit()

with open(argv[1], "r") as f:
    #Start by making a backup
    with open("dinkbak.ini", "w") as g:
        g.write(f.read())
    f.seek(0)
    lines = f.readlines()
    
with open(argv[1], "w") as f:
    for line in lines:
        if line.startswith("SET_SPRITE_INFO"):
            #print(lines)
            ssi = line.split()
            if ssi[1] == argv[2]:
                ssi[3] = argv[3]
                ssi[4] = argv[4]
                f.write(" ".join(ssi) + "\n")
                print(ssi)
        else:
            f.write(line)