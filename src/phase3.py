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
class Phase3:
    self.reviewsDB 
    self.ptermsDB
    self.rtermsDB
    self.scoresDB

    def __init__(self):
        self.reviewsDB = BDB('reviews.db', 'H') 
        self.ptermsDB = BDB('pterms.db', 'B+')
        self.rtermsDB = BDB('rterms.db', 'B+')
        self.scoresDB = BDB('scores.db', 'B+')

    def start(self):
        print("############# REVIEW LOOKUP SYSTEM #############")
        # while(1):
        query = input("Please provide a Query: ")
        parsedQuery = self.queryParser(query) 
        print(parsedQuery)
        listOfReviews = self.getReviews(parsedQuery)
        self.displayReviews(listOfReviews)


        self.reviewsDB.close()
        self.ptermsDB.close()
        self.rtermsDB.close()
        self.scoresDB.close()

    def displayReviews(self, listOfReviews):
        """

        """
        print("Here is the Result")
        print("")


    def getReviews(self, parsedQuery):
        """
        Using the parsedQuery data, intersects the conditional filters amongs the reviews.
        Until a filtered list of results is generated. 
        >>> p3  = Phase3()

        >>> parsedQuery = ([], [], [], [])
        >>> p3.getReviews(parsedQuery)
        []

        >>> parsedQuery = ([], [], [], [])
        >>> p3.getReviews(parsedQuery)
        []

        """
        list = []

        #Select by selections, selector = (selector, searchTerm)
        for entry in parsedQuery[2]:
            pass

        #Select by words, word = (searchTerm)
        for entry in parsedQuery[0]:
            pass

        #Select by wilds, wild = (searchTerm) 
        for entry in parsedQuery[1]:
            pass

        #Select by comparator, comparator = (comparator, operator, value)
        for entry in parsedQuery[3]:
            pass


        return list



    def queryParser(self, query):
        """
        Parser returns tuples containing 4 lists containng tuples.
        ([words], [wilds], [selectors], [comparators])

        word = (searchTerm)
        wild = (searchTerm)
        selector = (selector, searchTerm)
        comparator = (comparator, operator, value)


        >>> p3  = Phase3()
        
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
