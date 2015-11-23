# 1. p:camera The first query returns all records that have the term camera in the product title.

# 2. r:great The second query return all records that have the term great in the review summary or text.

# 3. camera The third query returns all records that have the term camera in one of the fields product title, review summary or review text.

# 4. cam% The fourth query returns all records that have a term starting with cam in one of the fields product title, review summary or review text. 

# 5. r:great cam% The fifth query returns all records that have the term great in the review summary or text and a term starting with cam in one of the fields product title, review summary or review text.

# 6. rscore > 4 The sixth query returns all records with a review score greater than 4

# 7. camera rscore < 3 The 7th query is the same as the third query except it returns only those records with a review score less than 3

# 8. pprice < 60 camera The 8th query is the same as the third query except the query only returns those records where price is present and has a value less than 60. Note that there is no index on the price field; this field is checked after retrieving the candidate records using conditions on which indexes are available (e.g. terms).

# 9. camera rdate > 2007/06/20 The 9th query returns the records that have the term camera in one of the fields product title, review summary or review text, and the review date is after 2007/06/20. Since there is no index on the review date, this condition is checked after checking the conditions on terms. Also the review date stored in file reviews.txt is in the form of a timestamp, and the date give in the query must be converted to a timestamp before a comparison (e.g. check out the date object in the datetime package for Python). 

# 10. camera rdate > 2007/06/20 pprice > 20 pprice < 60 Finally the last query returns the same set of results as in the 9th query except the product price must be greater than 20 and less than 60.

import re
import time
from IndexDB import *
from rgxHandler import *
from datetime import *
import operator

class Phase3:
    reviewsDB = None
    ptermsDB = None
    rtermsDB = None
    scoresDB = None

    rgx = None
    firstIntersectFlag = False

    def __init__(self):
        self.rgx = rgxHandler()

    def start(self):
        print("######################################################")
        print("############# PHASE 3 INITIALIZING QUERY #############")
        print("######################################################" + '\n')

        print("######################################################")
        print("#############    REVIEW LOOKUP SYSTEM    #############")
        #print("#############      "  + "Type 'q!' to quit"   +  "     #############")
        print("######################################################" + '\n')
        self.reviewsDB = IndexDB('rw.idx') 
        self.ptermsDB = IndexDB('pt.idx')
        self.rtermsDB = IndexDB('rt.idx')
        self.scoresDB = IndexDB('sc.idx')
        print("Type 'q!' to exit")

    def main(self):
        while(1):
            query = input("Please provide a Query: ")
            print("")
            if query == "q!":
                self.reviewsDB.close()
                self.ptermsDB.close()
                self.rtermsDB.close()
                self.scoresDB.close()
                exit()

            parsedQuery = self.queryParser(query) 
            # print(parsedQuery)
            listOfReviews = self.getReviews(parsedQuery)
            # print(listOfReviews)
            self.displayReviews(listOfReviews)

    def displayReviews(self, listOfReviews):
        
        i = 0
        for reviewKey in listOfReviews:
            i += 1
            reviewValue = self.reviewsDB.get(reviewKey)[0]
            #print(reviewValue)
            print("######################################################")
            print("#################      REVIEW " + str(i) +  "     #################")
            print("######################################################" + '\n')
            reviewValue = self.rgx.putLineTitlesBack(reviewValue)
            for line in reviewValue:
                if( "review/time" in line):
                    time =   datetime.fromtimestamp(float(line.split(":")[1].strip("\n").strip()))
                    print("review/time: " + time.strftime("%b %d %Y")+ "\n")

                else:
                    print(line, end='')
            print('\n')





    def getReviews(self, parsedQuery):
        """
        Using the parsedQuery data, intersects the conditional filters amongs the reviews.
        Until a filtered list of results is generated. 
        >>> p3  = Phase3()
        >>> p3.start()
        ######################################################
        ############# PHASE 3 INITIALIZING QUERY #############
        ######################################################
        <BLANKLINE>
        ######################################################
        #############    REVIEW LOOKUP SYSTEM    #############
        ######################################################
        <BLANKLINE>
        Type 'q!' to exit


        >>> parsedQuery = ([], [], [], [])
        >>> p3.getReviews(parsedQuery)
        []

        >>> parsedQuery = ([], [], [('r', 'ago')], [])
        >>> p3.getReviews(parsedQuery)
        ['9']

        >>> parsedQuery = (['ago'], [], [], [])
        >>> p3.getReviews(parsedQuery)
        ['9']

        >>> parsedQuery = (['again'], [], [], [])
        >>> p3.getReviews(parsedQuery)
        ['8', '10']

        >>> parsedQuery = (['again', 'used'], [], [], [])
        >>> p3.getReviews(parsedQuery)
        ['10']

        >>> parsedQuery = ([], ['ag'], [], [])
        >>> p3.getReviews(parsedQuery)
        ['8', '9', '10']

        >>> parsedQuery = (['again'], ['ag'], [], [])
        >>> p3.getReviews(parsedQuery)
        ['8', '10']

        >>> parsedQuery = ([], [], [], [('rdate', '<', '2000/01/01')])
        >>> p3.getReviews(parsedQuery)
        ['4', '5']

        >>> parsedQuery = ([], [], [], [('rdate', '<', '2000/01/01'), ('pprice', '<', '17')])
        >>> p3.getReviews(parsedQuery)
        ['5']


        >>> parsedQuery = (['cross'], [], [], [])
        >>> p3.getReviews(parsedQuery)
        ['5', '7', '8', '9', '10']

        >>> parsedQuery = ([], [], [('r', 'cross')], [])
        >>> p3.getReviews(parsedQuery)
        ['5', '7', '8', '10']

        >>> parsedQuery = ([], [], [('p', 'cross')], [])
        >>> p3.getReviews(parsedQuery)
        ['7', '8', '9', '10']


        >>> parsedQuery = ([], ['not'], [], [])
        >>> p3.getReviews(parsedQuery)
        ['1', '2', '8', '9']

        >>> parsedQuery = ([], ['not'], [('r', 'cross')], [])
        >>> p3.getReviews(parsedQuery)
        ['8']

        >>> parsedQuery = ([], [], [], [('rscore', '<', '5')])
        >>> p3.getReviews(parsedQuery)
        ['1', '3', '4']

        >>> parsedQuery = ([], [], [], [('rscore', '>', '4')])
        >>> p3.getReviews(parsedQuery)
        ['2', '5', '6', '7', '8', '9', '10']

        >>> parsedQuery = (['find'], [], [], [('rscore', '<', '5')])
        >>> p3.getReviews(parsedQuery)
        ['1', '4']

        >>> parsedQuery = ([], [], [], [('pprice', '<', '16')])
        >>> p3.getReviews(parsedQuery)
        ['5', '6']

        >>> parsedQuery = (['old'], [], [], [('pprice', '<', '16')])
        >>> p3.getReviews(parsedQuery)
        ['6']

        >>> parsedQuery = ([], [], [], [('rdate', '<', '2000/01/01')])
        >>> p3.getReviews(parsedQuery)
        ['4', '5']

        >>> parsedQuery = (['find'], [], [], [('rdate', '<', '2000/01/01')])
        >>> p3.getReviews(parsedQuery)
        ['4']

        >>> parsedQuery = ([], [], [], [('rdate', '>', '2000/01/01')])
        >>> p3.getReviews(parsedQuery)
        ['1', '2', '3', '6', '7', '8', '9', '10']

        >>> parsedQuery = ([], [], [], [('rdate', '>', '2009/01/01'), ('pprice', '>', '16'), ('pprice', '<', '18')])
        >>> p3.getReviews(parsedQuery)
        ['2']

        >>> parsedQuery = (['shazam'], [], [], [('rdate', '>', '2009/01/01'), ('pprice', '>', '16'), ('pprice', '<', '18')])
        >>> p3.getReviews(parsedQuery)
        []


        """
        self.firstIntersectFlag = False
        reviewList = []
        tmpList = []

        #Select by selections, selector = (selector, searchTerm)
        for entry in parsedQuery[2]:
            selector = entry[0]
            term = entry[1]

            if(selector == "r"):
                subList = self.rtermsDB.get(term)
                for i in subList:
                    tmpList.append(i)
            elif(selector == "p"):
                subList = self.ptermsDB.get(term)
                for i in subList:
                    tmpList.append(i)
            reviewList = self.ourIntersect(reviewList, tmpList)
            tmpList = []

            
        #Select by words, word = (searchTerm)
        for entry in parsedQuery[0]:
            subList = self.rtermsDB.get(entry)
            for i in subList:
                tmpList.append(i)

            subList = self.ptermsDB.get(entry)
            for i in subList:
                tmpList.append(i)

            reviewList = self.ourIntersect(reviewList, tmpList)
            tmpList = []

        #Select by wilds, wild = (searchTerm) 
        for entry in parsedQuery[1]:
            subList = self.rtermsDB.getWild(entry)
            for i in subList:
                tmpList.append(i)

            subList = self.ptermsDB.getWild(entry)
            for i in subList:
                tmpList.append(i)

            reviewList = self.ourIntersect(reviewList, tmpList)
            tmpList = []

        #Select by comparator, comparator = (comparator, operator, value)
        #pprice < 20
        #rdate > 2007/06/20 
        #rscore < 3 
        #product/price: unknown
        #review/score: 5.0
        #review/time: 1075939200


        for entry in parsedQuery[3]:

            comparator = entry[0]
            oper = entry[1]
            value = entry[2]

            ops = {"<": operator.lt, ">": operator.gt}

            if(comparator == "rdate"): 
                comparator = "rtime"
                year,month,day = value.split("/")
                try:
                    value = datetime(int(year), int(month), int(day))
                except:
                    print("Invalid Date Provided. No Results Found.")
                    return []
            else:
                value = value + ".0"

            keys = self.reviewsDB.getAllReviewKeys()
            for key in keys:
                item = self.rgx.putLineTitlesBack( self.reviewsDB.get(key)[0] )

                itemPrice = item[2].split(":")[1].strip("\n").strip()
                itemScore = item[6].split(":")[1].strip("\n").strip()
                itemDate = datetime.fromtimestamp( float(item[7].split(":")[1].strip("\n").strip() ))
                
                # print(itemPrice)
                # print(itemScore)
                # print(itemDate)
                # print("")

                comp_to_val = {"pprice": itemPrice, "rscore": itemScore, "rtime": itemDate }

                if ops[oper](comp_to_val[comparator], value) :
                    tmpList.append(key)

            reviewList = self.ourIntersect(reviewList, tmpList)
            tmpList = []


        # print(reviewList)
        return sorted(reviewList, key=float)

    def ourIntersect(self, b1, b2):
        if(not self.firstIntersectFlag):
            self.firstIntersectFlag = True
            return list(set(b2))
        else:
            return list(set(b1).intersection(b2))

    def queryParser(self, query):
        """
        Parser returns tuples containing 4 lists containng tuples.
        ([words], [wilds], [selectors], [comparators])

        word = (searchTerm)
        wild = (searchTerm)
        selector = (selector, searchTerm)
        comparator = (comparator, operator, value)

        >>> p3 = Phase3()
        
        >>> p3.queryParser("")
        ([], [], [], [])

        >>> result = p3.queryParser("P:caMeRa")
        >>> result[2]
        [('p', 'camera')]

        >>> result = p3.queryParser("r:grEaT")
        >>> result[2]
        [('r', 'great')]

        >>> result =p3.queryParser("cAmeRa")
        >>> result[0]
        ['camera']

        >>> result = p3.queryParser("cam%")
        >>> result[1]
        ['cam']

        >>> result = p3.queryParser("r:great cam%")
        >>> result[1]
        ['cam']
        >>> result[2]
        [('r', 'great')]

        >>> result = p3.queryParser("rscore > 4")
        >>> result[3] == [('rscore', '>', '4')]
        True

        >>> result = p3.queryParser("camera rscore < 3")
        >>> result[0]
        ['camera']
        >>> result[3] == [('rscore', '<', '3')]        
        True

        >>> result = p3.queryParser("pprice < 60 camera")
        >>> result[0]
        ['camera']
        >>> result[3] == [('pprice', '<', '60')]        
        True


        >>> result = p3.queryParser("camera rdate > 2007/06/20")
        >>> result[0]
        ['camera']
        >>> result[3] == [('rdate', '>', '2007/06/20')]        
        True

        >>> result = p3.queryParser("camera rdate > 2007/06/20 pprice > 20 pprice < 60")
        >>> result[0]
        ['camera']
        >>> result[3] == [('rdate', '>', '2007/06/20'), ('pprice', '>', '20'), ('pprice', '<', '60')]        
        True

        """  
        query = query.strip().lower().rstrip('\r\n')

        searchTerms = [] #(searchTerm)
        wildCardTerms = [] #(searchTerm)
        selectors = [] #(selector, searchTerm)
        comparators = [] #(comparator, operator, value)

        selector = re.compile(r"(r:|p:)[a-z]*")
        wild = re.compile(r"[a-z]*%")
        comparator = re.compile(r"\w*\s(<|>)\s[\w/]*")
        word = re.compile(r"[a-z]+")

        while(query != ""):
            # time.sleep(3)
            # print("looping query: " + query)
            query.strip().rstrip('\r\n')
            if(comparator.search(query)):
                found = comparator.search(query).group(0)
                query = query.replace(found, "")
                if(">" in found):
                    comparators.append( (found.split(">")[0].strip(),">",found.split(">")[1].strip()) )
                else:
                    comparators.append( (found.split("<")[0].strip(),"<",found.split("<")[1].strip()) )
                continue
            elif (selector.match(query)):
                # print("Selector found")
                found = selector.search(query).group(0)
                query = query.replace(found, "")
                selectors.append((found.split(":")[0],found.split(":")[1]))
                continue
            elif (wild.search(query)):
                # print("wild found")
                found = wild.search(query).group(0)
                query = query.replace(found, "")
                wildCardTerms.append(found.strip("%"))
                continue
            elif (word.search(query)):
                # print("Word found")
                found = word.search(query).group(0)
                query = query.replace(found, "")
                searchTerms.append(found)
                continue
            else:
                break

        return (searchTerms,wildCardTerms,selectors,comparators)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    p3 = Phase3()
    p3.start()
    p3.main()
