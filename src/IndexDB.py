from bsddb3 import db
from phase1 import *
from phase2 import *
from phase3 import *

class IndexDB:
    database = None
    name = None
    split_sign = ";"

    def __init__(self, name):
        # f = open(name, 'w')
        # f.close()
        self.name = name
        self.database = db.DB()
        # self.database.set_flags(db.DB_DUP)
        self.database.open(self.name)

    def get(self, key):
        """

        >>> p1 = Phase1("sample10.txt")
        >>> p1.start()
        ####### RUNNING PHASE 1 PARSING FILES #######
        <BLANKLINE>
        >>> p2 = Phase2()
        >>> p2.start()
        ####### RUNNING PHASE 2 CREATING INDEXES #######
        <BLANKLINE>

        >>> indexRW = IndexDB('pt.idx')

        >>> indexRW.get("chrono")
        ['10', '7', '8', '9']

        >>> indexRW.get("clothing")
        ['1']

        >>> indexRW.get("NOTHINGMATCHES")
        []

        

        """

        key = str.encode(key)
        list = []
        cur = self.database.cursor()

        if self.database.has_key(key) == True:
            # val = self.database[key]
            # val = self.database.get(key)
            val = cur.get(key, db.DB_SET)[1]
            # print(val)
            in_str = str(val,'ascii')
            list.append(in_str)
            count = cur.count()
            for i in range(count-1):
                val = cur.next_dup()[1]
                # print(val)
                in_str = str(val,'ascii')
                list.append(in_str)

        return list

    def getWild(self, key):
        """

        >>> p1 = Phase1("sample10.txt")
        >>> p1.start()
        ####### RUNNING PHASE 1 PARSING FILES #######
        <BLANKLINE>
        >>> p2 = Phase2()
        >>> p2.start()
        ####### RUNNING PHASE 2 CREATING INDEXES #######
        <BLANKLINE>

        >>> indexRW = IndexDB('pt.idx')

        >>> indexRW.getWild("ag%")
        ['8', '9', '10']

        """
        wildRE = re.compile(r''+key+'[a-z]*')

        key = str.encode(key)
        list = []
        cur = self.database.cursor()

        val = cur.first()
        while val:
            in_key = str(val[0],'ascii')
            in_val = str(val[1],'ascii')
            if re.match(wildRE, in_key):
                list.append(in_val)
            val = cur.next()

        return list

    def getAllReviewKeys(self):
        """

        >>> p1 = Phase1("sample10.txt")
        >>> p1.start()
        ####### RUNNING PHASE 1 PARSING FILES #######
        <BLANKLINE>
        >>> p2 = Phase2()
        >>> p2.start()
        ####### RUNNING PHASE 2 CREATING INDEXES #######
        <BLANKLINE>

        >>> indexRW = IndexDB('pt.idx')

        >>> indexRW.getWild("ag%")
        ['8', '9', '10']

        """
        wildRE = re.compile(r'[0-9]*')

        list = []
        cur = self.database.cursor()

        val = cur.first()
        while val:
            in_key = str(val[0],'ascii')
            in_val = str(val[1],'ascii')
            if re.match(wildRE, in_key):
                list.append(in_key)
            val = cur.next()

        return list

    def insert(self,key, value):
        if self.database.has_key(key)== False:
            self.database[key] = value
        else:
            val = str(self.database[key],'ascii')
            self.database[key] = val + self.split_sign + value

    def close(self):
        self.database.close()

    def remove(self, name):
        self.database.remove(name)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # p1 = Phase1("sample10.txt")
    # p1.start()
    # p2 = Phase2()
    # p2.start()

    # indexRW = IndexDB('pt.idx')
    # indexRW.get("chrono")

