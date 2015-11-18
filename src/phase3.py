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


class Phase3:

    def __init__(self):
    	pass

    def start(self):
    	query = raw_input("Please provide a Query: ")
    	#DO WORK
    	print("Here is the Result")






if __name__ == "__main__":
    p3 = Phase3()
    p3.start()
