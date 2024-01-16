"""A DMOD compressor that makes the '.dmod' tar.bz2 files that are commonly used to distribute Dink mods"""
import shutil
import os
import click
import glob

@click.command()
@click.argument("path")
@click.argument("outpath", default=".")
def pack(path, outpath):
	"""Packs a DMOD file and strips save files and shit"""
	#Maybe should prompt the user if they want to continue anyway even if there aren't any scripts or MAP.dat
	#This won't work on case-sensitive filesystems, I would wager.
	if os.path.exists(os.path.join(path, "story")):
		#Get the daymod's name
		name = os.path.basename(path)
		with open(os.path.join(path, "dmod.diz"), 'r') as f:
			title = f.readline()
			if "Skeleton" in title:
				#I seriously hope you don't forget to edit your details
				click.echo(click.style("You must edit DMOD.DIZ to include details about your mod", fg="red"))
				raise IOError
		click.echo("This appears to be a valid Dink Mod named %s" % title)
		#Check to see if there's a readme file and preview.bmp or maybe don't
		if not os.path.exists(os.path.join(path, "preview.bmp")):
			click.echo(click.style("Remember to include a 160x120 BMP file named preview.bmp that will show up in the DFarc list", fg="yellow"))

		if not os.path.exists("dist"):
			#Make an intermediary place to store stuff
			os.mkdir("dist")
		
		try:
			dest = shutil.copytree(path, os.path.join("dist", name))
		except:
			click.echo("Could not copy for some reason. Try running it again if it doesn't work.")
			dest = "dist"
		#Strip unnecessary files such as debug.txt, library.dat from WDE, skeleton.txt, clean.ini leftover from "INIclean", and saves
		stripmod(dest)
		#Compress it in to a file
		#I guess I don't really need to give it a name seeing as it's going to be renamed anyway but whatever
		arc = shutil.make_archive(name, "bztar", root_dir="dist", base_dir=name)
		#Rename it to a DMOD file and move it to the output location
		#if outpath != ".":
		shutil.move(arc, os.path.join(outpath, name + ".dmod"))
		#Delete the intermediary stuff
		shutil.rmtree(dest)
		click.echo("All done")

def stripmod(path):
	"""Takes a DMOD path and strips useless files from it"""
	files = ["debug.txt", "library.dat", "skeleton.txt", "clean.ini"]
	saves = glob.glob(os.path.join(path, "save*.dat"))
	files += saves

	for i in files:
		if os.path.exists(os.path.join(path,i)):
			os.remove(os.path.join(path,i))


if __name__ == '__main__':
	pack()