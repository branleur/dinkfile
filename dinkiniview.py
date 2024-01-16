"""Allows you to view a Dink Smallwood Dinkini and have a look at the sequences"""
#I hereby release this program into the public domain

import click
import pyglet
import os
import glob
import dfile.dinkini

curseq = 0

@click.command()
@click.argument("ini")
@click.argument("datapath")
def view(ini, datapath):
	"""Have a look at the stuff"""
	seqs = dfile.dinkini.readini(ini, datapath)

	window = pyglet.window.Window(800, 600, resizable=True, caption="Dink.ini Sequence Viewer")
	
	@window.event
	def on_draw():
		window.clear()
		#For the seq number display
		label = pyglet.text.Label(str(seqs[curseq]['number']), font_name="Times New Roman", font_size=36, x=50, y=0, anchor_x="center", anchor_y="bottom", color=(100,200,100,150))
		path = pyglet.text.Label(str(seqs[curseq]['path']), font_name="Helvetica", font_size=24, x=window.width//2, y=10, anchor_x="center", anchor_y="bottom")
		#Load the images in the sequence
		images = [pyglet.image.load(i) for i in seqs[curseq]['files']]
		#Set up our cursor for drawing placement
		cx, cy = 0, 0
		#Get the largest y value of the sequence so it doesn't go off the top of the screen
		if len(images) > 0:
			maxh = max([getattr(i, "height") for i in images])
			cy = window.height - maxh

		label.draw()
		path.draw()
		for count, i in enumerate(images):
			i.blit(cx, cy)
			#This seems to work okay although ideally it should use the actual filename or something
			seqnum = pyglet.text.Label(str(count+1), font_name="Arial", font_size=8, x=cx, y=cy, anchor_x="left", anchor_y="bottom", color=(255,10,9,255))
			seqnum.draw()
			#This should make it sort of wrap downwards
			if cx + i.width + 150 > window.width:
				cy -= maxh
				cx = 0
			else:
				cx += i.width

	@window.event
	def on_key_press(sym, mod):
		global curseq
		#Set up key bindings to change shit.
		if sym == pyglet.window.key.LEFT:
			curseq -= 1
		elif sym == pyglet.window.key.RIGHT:
			#Check that we're not at the end
			if curseq + 1 > len(seqs) -1:
				curseq = 0
			else:
				curseq += 1

	pyglet.app.run()

if __name__ == '__main__':
	view()