#the engine to all the things

#this contains all the methods required for k nearest neighbour filter
# import k_nearest_neighbour_filter

#this contains all the methods required for content based filter 
# import content_based__filter

#this conatins all the methods required for collarative 2nd filter
# import collaborative_2nd_filter

#sql library
import pymysql

###########---program starts here---###########

password = input("enter the password - ")

db = pymysql.connect("localhost","root",password,"newMovieLens" )
cursor = db.cursor()

query_all_the_user_rating = "select * from newRating"

cursor.execute(query_all_the_user_rating)
all_the_user_rating = cursor.fetchall()
for i in cursor.fetchall():
	ipasds = 1
# k_nearest_neighbour_filter()

# content_based_filter()

# collaborative_filter()