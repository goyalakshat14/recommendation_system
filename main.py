#the engine to all the things

#this contains all the methods required for k nearest neighbour filter
import k_nearest_neighbour_filter as knn

#this contains all the methods required for content based filter 
import content_based__filter as cbf

#this conatins all the methods required for collarative 2nd filter
import npmi_filter as npmi

#sql library
import pymysql

import time

#this returns a dictionary with key movies that have their genre stored as key of nested dictionary
def get_movies_with_genre(cursor):
	query = "select * from genre"
	cursor.execute(query)
	genre = cursor.fetchall()
	movie_with_genre = {}
	for movie in genre:
		if(movie[0] in movie_with_genre):
			movie_with_genre[movie[0]].update({movie[1]})
		else:
			movie_with_genre[movie[0]] = {movie[1]}
	return movie_with_genre

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

def get_the_count_of_genre(cursor):
	query = "select count(distinct genre) from genre"
	cursor.execute(query)
	return cursor.fetchone()[0]

#input all_the_user_rating is a dict of user which has a nested
#	dictionary that has a movie as key and value as rating
def get_count_and_list_of_user_rated_movie(all_the_user_rating):
	count_and_list_of_user_rated_movie = {}
	for user in all_the_user_rating:
		for movie in all_the_user_rating[user]:
			if(movie in count_and_list_of_user_rated_movie):
				count_and_list_of_user_rated_movie[movie][0] += 1
				count_and_list_of_user_rated_movie[movie][1].update({user})
			else:
				count_and_list_of_user_rated_movie[movie] = [1,{user}]
	return count_and_list_of_user_rated_movie
###########---program starts here---###########

uid = 1
no_of_rated_movies_fetch = 200
no_of_users_fetch = 200
no_of_unrated_movies = 200

password = input("enter the password - ")

db = pymysql.connect("localhost","root",password,"newMovieLens" )
cursor = db.cursor()

starting_time = time.time()

all_the_user_rating = get_all_the_rating_and_user(cursor)
# time_elapsed_to_get_user_data = time.time() - starting_time

movie_with_genre = get_movies_with_genre(cursor)
# time_elapsed_to_get_genre = time.time() - starting_time 

count_of_genre = get_the_count_of_genre(cursor)

count_and_list_of_user_rated_movie = get_count_and_list_of_user_rated_movie(all_the_user_rating)
print(time.time()-starting_time)
#knn filter
rated_movie_users,rated_movie,unrated_movie,predicted_movie_rating = knn.k_collab_filter_program_controller(starting_time,cursor,uid,no_of_rated_movies_fetch,no_of_users_fetch,no_of_unrated_movies,all_the_user_rating)
print("got predictrive rating",time.time()-starting_time)
# time_elapsed_to_get_data_from_first_filter = time.time() - starting_time 

#genre based content filter
damping_factor = cbf.content_based_filter_controller(all_the_user_rating,rated_movie,unrated_movie,count_of_genre,movie_with_genre,cursor)
# time_elapsed_to_get_data_from_second_filter = time.time() - starting_time
print("startng npmi",time.time()-starting_time)
#nmpi filter
npmi_factor = npmi.npmi_filter_program_controller(starting_time,all_the_user_rating,count_and_list_of_user_rated_movie,rated_movie,unrated_movie)
print("npmi over",time.time()-starting_time)

# collaborative_filter()