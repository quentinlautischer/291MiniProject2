import subprocess
from b_bsddb3 import *
from bsddb3 import db
from TimeWrapper import timed
#call(["ls", "-l"])

class Phase2:
    reviews = ("reviews.txt", "rw.idx")
    pterms = ("pterms.txt", "pt.idx")
    rterms = ("rterms.txt", "rt.idx")
    scores = ("scores.txt", "sc.idx")
    sortFiles = [pterms, rterms, scores]

    def __init__(self):
        try:
            subprocess.check_output("rm -rf rw.idx", stderr=subprocess.STDOUT, shell=True)
        except:
            print("Issue cleaning up. DONT BE A FOOL.")
        try:
            subprocess.check_output("rm -rf pt.idx", stderr=subprocess.STDOUT, shell=True)
        except:
            print("Issue cleaning up. DONT BE A FOOL.")    
        try:
            subprocess.check_output("rm -rf rt.idx", stderr=subprocess.STDOUT, shell=True)   
        except:
            print("Issue cleaning up. DONT BE A FOOL.")
        try:
            subprocess.check_output("rm -rf sc.idx", stderr=subprocess.STDOUT, shell=True)
        except:
            print("Issue cleaning up. DONT BE A FOOL.")
    @timed
    def start(self):
        print("####### RUNNING PHASE 2 CREATING INDEXES #######")
        print("")
        for filename, idx in self.sortFiles:
            subprocess.check_output("sort -u -o " + filename + " " + filename, stderr=subprocess.STDOUT, shell=True)
            
            self.updateFileStructure(filename)

            subprocess.check_output("db_load -c duplicates=1 -T -t btree -f " + filename + " " + idx, stderr=subprocess.STDOUT, shell=True)
        
        self.updateFileStructure(self.reviews[0])
        subprocess.check_output("db_load -T -t hash -f " + self.reviews[0] + " " + self.reviews[1], stderr=subprocess.STDOUT, shell=True)
    @timed
    def updateFileStructure(self, filename):
        lines = self.parseFile(filename)
        self.overWrite(filename, lines)
    @timed
    def parseFile(self, filename):
        f = open(filename)
        linesout = []

        for line in f:
            lineed = line.split(',', 1)
            linesout.append(lineed[0] + '\n')
            linesout.append(lineed[1])
        f.close()
        return linesout
    @timed
    def overWrite(self, filename, lines):
        f = open(filename, 'w')
        for line in lines:
            f.write(line)
        f.close()
        
if __name__ == "__main__":
    p2 = Phase2()
    p2.start()
