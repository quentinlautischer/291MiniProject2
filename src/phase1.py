from rgxHandler import *
from rgxHandler import * 

class phase1:

	def __init__(self, filename):
		this.filename = filename

	def parseFile(self):
		rgx = rgxHandler()

		f = open(this.filename)
		linesout = []
		i = 0
		k = 0

		for line in f:
			if i == 0:
				linesout.append(str(k + 1) + ',')
				linesout.append(rgx.line_rgx(line) + ',')
				i+=1
			elif i in [1, 3, 4, 6, 7, 8]:
				linesout.append(rgx.line_rgx(line) + ',')
				i+=1
			elif i in [2, 5, 9]:
				if i == 9:
					linesout.append('"' + rgx.line_rgx(line) + '"')
				else:
					linesout.append('"' + rgx.line_rgx(line) + '"' + ',')
				i+=1
			else:
				i=0
		return linesout
		
	

	def printReviews(self, lines):
		output = null
		i = 0
		
		for line in lines:
			output = output + line
			if i == 9:
				output = ouput + '\n'
				i = 0
			else:
				i += 1
		output = open("reviews.txt", "w")
	    output.write(line)
	

	def printPterms(self, lines):
        i = 2
        

	def printRterms(self, lines):

	def printScores(self, lines):	
