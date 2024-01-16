#Licensed under the WTFPL. You just do what the fuck you want to
"""Mapstats for Dink Smallwood tells you useless shit about your Dink map files"""

import argparse
import os
import sys
from statistics import mode
import dfile.mapdat

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("map", help="The map file you'd like to inspect")
	print("Welcome to DinkMapStats\n")
	args = parser.parse_args()
	mapfile = dfile.mapdat.readmap(args.map)
	print("Amount of screens: %s" % len(mapfile))
	sprites = 0
	scripsprites = 0
	invis = 0
	spritescrip = []
	scrscript = 0
	scriptscr = []
	tile = []
	for screen in mapfile:
		for sprite in screen['sprites']:
			if sprite['active'] == 1:
				sprites += 1
			if len(sprite['script']) > 0:
				scripsprites += 1
				spritescrip.append(sprite['script'])
		for tiles in screen['tileno']:
			tile.append(tiles)

		if len(screen['script']) > 0:
			scrscript += 1
			scriptscr.append(screen['script'])


	print("Total sprites in use: %s" % sprites)
	print("Total sprites with scripts attached: %s" % scripsprites)
	print("Most commonly used map tile number: {0}".format(mode(tile)))
	print("Number of screens with sprites attached: {0}".format(scrscript))
	print("Most commonly attached screen script: {0}".format(mode(scriptscr)))

if __name__ == '__main__':
	main()