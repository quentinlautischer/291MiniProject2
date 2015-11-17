import subprocess
from b_bsddb3 import *
from bsddb3 import db
#call(["ls", "-l"])

class Phase2:
    reviews = ("reviews.txt", "rw.idx")
    pterms = ("pterms.txt", "pt.idx")
    rterms = ("rterms.txt", "rt.idx")
    scores = ("scores.txt", "sc.idx")
    #sortFiles = [pterms, rterms, scores]
    sortFiles = [reviews, pterms, rterms, scores]

    reviewsDB = None
    ptermsDB = None
    rtermsDB = None
    scoresDB = None

    def __init__(self):
        print("DB Inits")
        b = db.DB()
        try:
            subprocess.run("rm -rf rw.idx", shell=True, check=True)
            b.remove("reviews.db")
        except:
            pass
        try:
            subprocess.run("rm -rf pt.idx", shell=True, check=True)
            b.remove("pterms.db")
        except:
            pass    
        try:
            subprocess.run("rm -rf rt.idx", shell=True, check=True)   
            b.remove("rterms.db")
        except:
            pass
        try:
            subprocess.run("rm -rf sc.idx", shell=True, check=True)
            b.remove("scores.db")
            
        except:
            pass

        self.reviewsDB = BDB('reviews.db', 'H') 
        self.ptermsDB = BDB('pterms.db', 'B+')
        self.rtermsDB =  BDB('rterms.db', 'B+')
        self.scoresDB = BDB('scores.db', 'B+')

    def start(self):
        print("#Creating Indexes")
        for filename, idx in self.sortFiles:
            subprocess.run("sort -u -o " + filename + " " + filename, shell=True, check=True)
            subprocess.run("db_load  -c duplicates=1 -T -t btree -f " + filename + " " + idx, shell=True, check=True)


        print("Closing DB's")

        self.reviewsDB.close()
        self.ptermsDB.close()
        self.rtermsDB.close()
        self.scoresDB.close()
        


if __name__ == "__main__":
    p2 = Phase2()
    p2.start()