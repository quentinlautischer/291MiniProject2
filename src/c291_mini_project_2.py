import phase1
import phase2
import phase3 

import os
import sys


inputfile = input("Please provide your review file: ")
while(not os.path.exists(inputfile)):
	print("Failed, path does not exist.")
	inputfile = input("Please provide your review file: ")


# p1 = Phase1("sample10.txt")

p1 = phase1.Phase1(inputfile)
p2 = phase2.Phase2()
p3 = phase3.Phase3()



p1.start()
p2.start()
p3.start()
p3.main()







			
