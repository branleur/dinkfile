"""Reads Dink.ini files and all of that sort of thing hopefully"""
#There are load_sequence lines, set_frame_frame lines, set_frame_special lines, set_frame_delay lines, along with SET_SPRITE_INFO lines. All the parsing should be case-insensitive
import glob
import os

def readini(inifile, path="."):
	"""Reads a Dink.ini file and attempts to get data out of it. Returns a list containing the sequences."""
	seqs = []
	with open(inifile, "r") as f:
		for line in f:
			if line.lower().startswith("load_sequence"):
				seq = {}
				seq['number'] = line.split()[2]
				seq['path'] = line.split()[1]
				#Some lines don't have certain attributes because they don't animate
				if len(line.split()) > 5:
					#This may also be an uppercase attribute like black or leftalign for the interface graphics
					seq['delay'] = line.split()[3]
					seq['x'] = line.split()[4]
					seq['y'] = line.split()[5]
					#seq['square'] = line.split()[6,7,8,9]
				#prefix = line.split()[1].split("\\")[-1]
				#Change the file extension to an asterisk to make it file-type agnostic
				seq['files'] = glob.glob(os.path.join(path, seq['path'] + "*.bmp"))
				seqs.append(seq)
			elif line.upper().startswith("SET_FRAME_FRAME"):
				cmd, destseq, destframe, srcseq = line.split()[0:4]
				#Minus one means the sequence is to repeat
				if srcseq != "-1":
					srcframe = line.split()[4]
					#Find the source frame's path and add it to the dest seq/frame
					for i in seqs:
						if i['number'] == srcseq:
							for k in seqs:
								if k['number'] == destseq:
									if len(k['files']) > int(destframe) - 1:
										k['files'][int(destframe) -1] = i['files'][int(srcframe) -1] 
									elif int(destframe) > len(k['files']):
									#Presumably this might work or something
										#print(line, i['files'], int(srcframe)-1, "\n")
										try:
											k['files'].append(i['files'][int(srcframe) -1])
										except:
											#Warn the user or something
											pass

				else:
					#pete and repete were in a boat. Pete jumped out. Who was left?
					pass

	return seqs