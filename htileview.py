"""A small program that allows you to specify a HARD.DAT file to view the collision tiles on screen. Not particularly polished but it still works."""
import pygcurse
import pygame
from pygame.locals import *
from sys import argv, exit
from dfile.harddat import openhdat

YELLOW = (255, 232, 18)
RED = (255, 0, 0)
BLUE = (13, 142, 255)
BLACK = (0, 0, 0)

def main():
    if len(argv) < 2:
        print("Specify a hard.dat file path to view it")
    else:
        try:
            hdat = openhdat(argv[1])
        except:
            print("Oh noes something went wrong")

    main = pygcurse.PygcurseWindow(52,51, "Collision Tiles")
    main.autoblit = False
    square = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    square = 0
                elif event.key == K_RIGHT:
                    square += 1
                elif event.key == K_LEFT:
                    square -= 1
                
                x = 0
                y = 0

                pygame.display.set_caption("Collision Tile #%s" % square)
                for i, j in enumerate(hdat[square]):
                    if j == 0:
                        main.bgcolor = 'black'
                        main.write("N", x=x, y=y)
                    elif j == 1:
                        main.bgcolor = 'yellow'
                        main.write("H", x=x, y=y)
                    elif j == 2:
                        main.bgcolor = 'blue'
                        main.write("L", x=x, y=y)
                    elif j == 3:
                        main.bgcolor = 'red'
                        main.write("?", x=x, y=y)
                    else:
                        main.bgcolor = 'fuchsia'
                        main.write("@")

                    if y > 1 and y % 50 == 0:
                        x += 1
                        y = 0
                    else:
                        y += 1
                main.blittowindow()



if __name__ == '__main__':
    main()