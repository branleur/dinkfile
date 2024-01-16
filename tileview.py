"""Tileview. View the numbers of individual tiles"""
#This is my first attempt at writing something useful with Pyglet so be warned.

import pyglet
import glob
from sys import argv
import os

curtile = 0
pyglet.clock.set_fps_limit(5)

if argv[1]:
	if os.path.exists(argv[1]):
		#Check to see if it has tiles in it
		#TODO: Allow user to specify refdir and DMOD path separately
		os.chdir(argv[1])
		tiles = glob.glob("[Tt][Ss]*.*")
		#ima = [pyglet.image.load(i) for i in tiles]
		ima = []
		for i in tiles:
			#The relatively high RAM usage is probably because of this. All the tile screens are loaded at once here.
			ima.append(pyglet.image.load(i))

		#Apparently the tile sheets can be bigger according to Magicman but I will leave the window at this size for common use
		window = pyglet.window.Window(width=600, height=400, caption="Dink Tile View")

		@window.event
		def on_key_press(symbol, mod):
			#print("FPS is %f" % pyglet.clock.get_fps())
			global curtile
			if symbol == pyglet.window.key.LEFT:
				if curtile == 0:
					curtile = 0
				else:
					curtile = curtile - 1
			elif symbol == pyglet.window.key.RIGHT:
				if curtile == len(ima) - 1:
					curtile = 0
				else:	
					curtile = curtile + 1
		
		

		@window.event
		def on_draw():
			window.clear()
			ima[curtile].blit(0,0)
			#Draw the current tile screen number in the middle of the screen
			scrno = pyglet.text.Label(str(curtile + 1), font_name="Arial", font_size=24, x = window.width / 2, y = window.height / 2, anchor_x= "center", anchor_y = "center", color=(225, 0, 9, 150))
			scrno.draw()
			#Draw the current tile number on each tile
			#Tiles start from the top left, while the draw coordinate in Pyglet starts from the bottom left meaning the Y value has to be changed.
			y = ima[curtile].height
			x = 0
			count = 0
			for i in range(8):
				if count > 0:
					y -= 50
					x = 0
				for i in range(12):
					tilnum = pyglet.text.Label(str(count + (curtile * 128)), font_name="Times", font_size=14, x=x, y=y, anchor_x= "left", anchor_y = "top", color=(232,153,11, 255))
					tilnum.draw()
					count += 1
					x += 50

		pyglet.app.run()
	else:
		print("Your path doesn't appear to be valid")
else:
	print("Provide your Dink tiles path to view their numbering")

