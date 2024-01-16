"""Dink.ini sprite checker looks to see how many lines of stuff there is in the file and can strip excess set sprite info lines or at least maybe it will in the next release."""
import click

@click.command()
@click.argument("dinkini")
@click.option("--outfile", default="dink.ini")
def iniread(dinkini, outfile):
	#Maximum sequences in Dink 1.08 is 1000 (1.09 is 1300). Maximum sprite info lines is 1000 in 1.08 (no limit in 1.09). Max sprites is 4000 (6000 in 1.09)
	with open(dinkini, "r") as f:
		seq = []
		sprinfo = []
		for line in f:
			#Convert them to uppercase because the engine doesn't care and neither do users
			if line.upper().startswith("LOAD_SEQUENCE"):
				seq.append(line)
			elif line.upper().startswith("SET_SPRITE"):
				sprinfo.append(line)

		click.echo("You have %d sprite lines out of 1000 (1300 in 1.09) and %d sprite info lines out of 1000 (irrelevant in 1.09)" % (len(seq), len(sprinfo)))

		f.seek(0)
		sprinfo.sort()
		newinfo = list(sprinfo)
		for count, line in enumerate(sprinfo):
			inf = line.split(" ")
			previnf = sprinfo[count -1].split(" ")
			if inf[1] == previnf[1] and inf[2] == previnf[2]:
				#Make sure it deletes the previous line so that it keeps the newest one
				newinfo.remove(sprinfo[count-1])

		click.echo(click.style("Found %d redundant sprite info lines" % (len(sprinfo) - len(newinfo)), fg="yellow"))
		if input("Would you like to remove excess lines?").upper() == "yes":
			#Crop the lines here
			...


if __name__ == '__main__':
	iniread()