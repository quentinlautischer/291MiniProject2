from b_bsddb3 import *
from rgxHandler import * 

rgx = rgxHandler()
f = open("sample10.text")

p1 = phase1()
p2 = phase2()
p3 = phase3()


p1.start()
p2.start()
p3.start()


#getrids = ["product/productId: ", "product/title: ", "product/price: ", "review/userId: ", "review/profileName: ", "review/helpfulness: ", "review/score:",
#	"review/time: ", "review/summary:", "review/text: "]
linesout = []




i = 0
k = 0

for line in f:
	#li = (line.strip('\n'))
	if i == 0:
		linesout.append(str(k + 1) + ',')
		#linesout.append(re.sub(getrids[i], '', line.strip('\n')) + ',')
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
	

	
output = open("pythonoutput.text", "a")

for line in linesout:
	output.write(line);


			
