import pymysql

def get_all_the_rating_and_user(cursor):
	query_all_the_user_rating = "select * from newRating"
	cursor.execute(query_all_the_user_rating)
	all_the_user_rating = cursor.fetchall()
	user_dict = {}
	for user in all_the_user_rating:
		if(user[0] in user_dict):
			user_dict[user[0]].update({user[1]:user[2]})
		else :
			user_dict[user[0]] = {user[1]:user[2]}

	return user_dict

#this returns a dictionary with key movies that have their genre stored as key of nested dictionary
def get_movies_with_genre(cursor):
	query = "select * from genre"
	cursor.execute(query)
	genre = cursor.fetchall()
	movie_with_genre = {}
	for movie in genre:
		if(movie[0] in movie_with_genre):
			movie_with_genre[movie[0]].update({movie[1]:''})
		else
			movie_with_genre[movie[0]] = {movie[1]:''}
	return movie_with_genre

def content_based_filter():
	print("will do something")
	
def content_based_filter_controller():
	movie_with_genre = get_movies_with_genre(cursor)






#testing contetn based filter
uid = 1
no_of_rated_movies_fetch = 200
no_of_users_fetch = 200
no_of_unrated_movies = 200

password = input("enter the password - ")

db = pymysql.connect("localhost","root",password,"newMovieLens" )
cursor = db.cursor()
all_the_user_rating = get_all_the_rating_and_user(cursor)

content_based_filter_controller(all_the_user_rating,cursor)
