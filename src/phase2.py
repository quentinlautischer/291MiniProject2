import subprocess
from b_bsddb3 import *
#call(["ls", "-l"])

class Phase2:
    reviews = "reviews.txt"
    pterms = "pterms.txt"
    rterms = "rterms.txt"
    scores = "scores.txt"
    sortFiles = [pterms, rterms, scores]

    reviewsDB = None
    ptermsDB = None
    rtermsDB = None
    scoresDB = None

    def __init__(self):
        self.reviewsDB = BDB('pterms.db',"H") 
        self.ptermsDB = BDB('pterms.db',"B+")
        self.rtermsDB =  BDB('rterms.db',"B+")
        self.scoresDB = BDB('scores.db',"B+")

    def start(self):
        for filename in self.sortFiles:
            subprocess.run("sort -u -o " + filename + " " + filename, shell=True, check=True)




if __name__ == "__main__":
    p2 = Phase2()
    p2.start()
