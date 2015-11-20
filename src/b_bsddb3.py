#import bsddb3
from bsddb3 import db
# Davood's file
# Updated by Kriti
# Command to run: python b_bsddb3.py
class BDB:
    database = None
    split_sign = ";"
    dbType = db.DB_UNKNOWN

    def __init__(self, name, dbType):
        if dbType == 'B+':
            self.dbType = db.DB_BTREE  
        else:
            self.dbType = db.DB_HASH

        self.database = db.DB()
        #self.database.set_flags(db.DB_DUP)
        self.database.open(name, None, self.dbType, db.DB_CREATE)

    def get(self,key):
        if self.database.has_key(key) == True:
            val = self.database[key]
            in_str = str(val,'ascii')
            #print(in_str)
            return in_str.split(self.split_sign)
        else:
            return  []

    def insert(self,key, value):
        if self.database.has_key(key)== False:
            self.database[key] = value
        else:
            val = str(self.database[key],'ascii')
            self.database[key] = val + self.split_sign + value

    def getAll(self): 
        cur = self.database.cursor() 
        iter = cur.first()
        while iter:
            print(iter)
            iter = cur.next()
        cur.close()

    def close(self):
            self.database.close()
    
    def remove(self, name):
            self.database.remove(name)      

####################
#DATABASE = 'f112.db'
#x = BDB(DATABASE)
#x.insert(b'1',"apple")
#x.insert(b'1',"pear")
#x.insert(b'1',"grapes")
#y = x.get(b'1')
#print(y)
