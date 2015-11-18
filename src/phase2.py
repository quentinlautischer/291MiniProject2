import subprocess
from b_bsddb3 import *
from bsddb3 import db
#call(["ls", "-l"])

class Phase2:
    reviews = ("reviews.txt", "rw.idx")
    pterms = ("pterms.txt", "pt.idx")
    rterms = ("rterms.txt", "rt.idx")
    scores = ("scores.txt", "sc.idx")
    sortFiles = [pterms, rterms, scores]

    reviewsDB = None
    ptermsDB = None
    rtermsDB = None
    scoresDB = None

    def __init__(self):
        print("DB Inits")
        b = db.DB()
        try:
            subprocess.check_output("rm -rf rw.idx", stderr=subprocess.STDOUT, shell=True)
            # b.remove("reviews.db")
        except:
            print("Issue cleaning up. DONT BE A FOOL.")
        try:
            subprocess.check_output("rm -rf pt.idx", stderr=subprocess.STDOUT, shell=True)
            # b.remove("pterms.db")
        except:
            print("Issue cleaning up. DONT BE A FOOL.")    
        try:
            subprocess.check_output("rm -rf rt.idx", stderr=subprocess.STDOUT, shell=True)   
            # b.remove("rterms.db")
        except:
            print("Issue cleaning up. DONT BE A FOOL.")
        try:
            subprocess.check_output("rm -rf sc.idx", stderr=subprocess.STDOUT, shell=True)
            # b.remove("scores.db")
        except:
            print("Issue cleaning up. DONT BE A FOOL.")

        self.reviewsDB = BDB('reviews.db', 'H') 
        self.ptermsDB = BDB('pterms.db', 'B+')
        self.rtermsDB =  BDB('rterms.db', 'B+')
        self.scoresDB = BDB('scores.db', 'B+')

    def start(self):
        print("#Creating Indexes")
        for filename, idx in self.sortFiles:
            subprocess.check_output("sort -u -o " + filename + " " + filename, stderr=subprocess.STDOUT, shell=True)
            subprocess.check_output("db_load -c duplicates=1 -T -t btree -f " + filename + " " + idx, stderr=subprocess.STDOUT, shell=True)
        
        subprocess.check_output("db_load -c duplicates=1 -T -t hash -f " + self.reviews[0] + " " + self.reviews[1], stderr=subprocess.STDOUT, shell=True)

        print("Closing DB's")

        self.reviewsDB.close()
        self.ptermsDB.close()
        self.rtermsDB.close()
        self.scoresDB.close()
        


if __name__ == "__main__":
    p2 = Phase2()
    p2.start()