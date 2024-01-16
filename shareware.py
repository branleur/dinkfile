import pygcurse

def main():
    lose = pygcurse.PygcurseWindow(caption="Dink Smallwood")
    lose.fill(bgcolor="red", fgcolor='yellow')
    lose.write("Dink Smallwood: A cool game from ", x=9, bgcolor="red", fgcolor="yellow" )
    lose.write("RTSoft", fgcolor="blue")
    #lose.putchars("-" * 80, fgcolor="yellow", y=1, x= 0)
    lose.drawline(start_pos = (0,1), end_pos = (80,1), bgcolor="yellow")
    lose.putchars("Sure, don't order Dink Smallwood. Let The Cast and the Dead Dragon Carcass Cult take over the king's realm. Don't face the cool bonca or the utterly hilarious end boss", x=0, y=2)
    lose.putchars("Or you can man up and attempt to fuck your aunt after killing your uncle. Order the full version of Dink Smallwood!", y=5, x=0)
    lose.putchars("To order Dink, simply visit HTTP://RTSOFT.COM in your web browser", y = 8, x= 0)

    pygcurse.waitforkeypress()


if __name__ == '__main__':
    main()