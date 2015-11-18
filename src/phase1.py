from rgxHandler import *

class phase1:

	def __init__(self, filename):
		self.filename = filename
		self.lines = self.parseFile()
		print(len(self.lines))

	def parseFile(self):
		rgx = rgxHandler()

		f = open(self.filename)
		linesout = []
		i = 0
		k = 0

		for line in f:
			lineed = rgx.line_rgx(line)
			if i == 0:
				linesout.append(str(k + 1) + ',')
				linesout.append(lineed + ',')
			elif i in [2, 3, 5, 6, 7]:
				linesout.append(lineed + ',')
			elif i in [1, 4, 8, 9]:
				if i == 9:
					linesout.append('"' + lineed + '"')
				else:
					linesout.append('"' + lineed + '"' + ',')
			else:
				i=-1
				k+=1
			i+=1
		return linesout
	
	def start(self):
		self.createFiles()

	
	def createFiles(self):
		review = ""
		self.clearFiles()
		reviews, outputp, outputr, outputs = self.OpenFiles()

		i = 0
		k = 1

		for line in self.lines:
			review += line
			if i == 2:
				self.writeToFile3(line, outputp, k, i) #Write P terms
			elif i == 7:
				if(k != (len(self.lines)/11)):
					outputs.write(line + str(k) + '\n') #Writing scores
				else:
					outputs.write(line + str(k))
			elif i == 9:
				self.writeToFile3(line, outputr, k, i) #Writing R terms
			elif i == 10:
				self.writeToFile3(line, outputr, k, i) #Writing R terms
				if(k != (len(self.lines)/11)):
					review += '\n'
				i = -1
				k += 1
			else:
				pass
			
			i += 1
		reviews.write(review) #Write review

	def writeToFile3(self, line, outfile, k, i):
		rgx = rgxHandler()
		words = rgx.find3OrMore(line)
		for word in words:
			#outfile.write(word + ',' + str(k) + '\n')
			if(k == (len(self.lines)/11) and word == words[-1] and (i == 10 or i == 2)):
				outfile.write(word + ',' + str(k))
			else:
				outfile.write(word + ',' + str(k) + '\n') #Also Write the term we want

	def OpenFiles(self):
		outputp = open("pterms.txt", "a") #Open Files
		outputr = open("rterms.txt", "a")
		outputs = open("scores.txt", "a")
		reviews = open("reviews.txt", "w")

		return (reviews, outputp, outputr, outputs)

	def clearFiles(self):
		self.deleteContent("pterms.txt") 
		self.deleteContent("rterms.txt")
		self.deleteContent("scores.txt")
		self.deleteContent("reviews.txt")


	def deleteContent(self, fName):
		f = open(fName, "w")
		f.close()
