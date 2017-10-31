#the engine to all the things
from bottle import route, run, request, hook, response

import json
#this contains all the methods required for k nearest neighbour filter
import k_nearest_neighbour_filter as knn

#this contains all the methods required for content based filter 
import content_based__filter as cbf

#this conatins all the methods required for npmi(normalized pointwise mutual information) filter
import npmi_filter as npmi

#this contains all the methods required for tag based filter
import tag_based_filter as tbf
#sql library
import pymysql

import time

import operator

import getpass
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

def get_all_movie_title(cursor):
	movie_title = {}
	query = "select * from movie"
	cursor.execute(query)
	titles = cursor.fetchall()
	for title in titles:
		movie_title[title[0]] = title[1]
	return movie_title

def get_all_the_rating_and_user(cursor):
	query_all_the_user_rating = "select * from newRating"
	cursor.execute(query_all_the_user_rating)
	all_the_user_rating = cursor.fetchall()
	user_dict = {}
	for user in all_the_user_rating:
		if(user[0] in user_dict):
			user_dict[user[0]].update({user[1]:float(user[2])})
		else :
			user_dict[user[0]] = {user[1]:float(user[2])}
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

def get_tag_relav(cursor):
	movie_tag = {}
	tag_relav = {}
	query = "select * from tag_relav"
	cursor.execute(query)
	all_tag = cursor.fetchall()
	for movie in all_tag:
		if(movie[0] in tag_relav):
			tag_relav[movie[0]].update({movie[1]:float(movie[2])})
			movie_tag[movie[0]].update({movie[1]})
		else:
			tag_relav[movie[0]] = {movie[1]:float(movie[2])}
			movie_tag[movie[0]] = {movie[1]}
	return tag_relav,movie_tag

#we are subtracrting from 1 to get dissimilarity
def dissim_config(unrated_movie,movie_title,predicted_movie_rating,genre_factor,npmi_factor,popularity_factor,tag_based_factor):
	recom_list = {}
	for movie in unrated_movie:
		rating = predicted_movie_rating_weight*predicted_movie_rating[movie]+genre_factor_weight*(1-genre_factor[movie])+npmi_factor_weight*(1-npmi_factor[movie])+popularity_factor_weight*(1-popularity_factor[movie])+tag_based_factor_weight*(1-tag_based_factor[movie])
		recom_list[movie_title[movie]] = rating
	recom_list = sorted(recom_list.items(), key=operator.itemgetter(1), reverse=True)
	return recom_list

def mixed_config(unrated_movie,movie_title,predicted_movie_rating,genre_factor,npmi_factor,popularity_factor,tag_based_factor):
	recom_list = {}
	for movie in unrated_movie:
		rating = predicted_movie_rating_weight*predicted_movie_rating[movie]+genre_factor_weight*(max([1-genre_factor[movie],genre_factor[movie]]))+npmi_factor_weight*(max([1-npmi_factor[movie],npmi_factor[movie]]))+popularity_factor_weight*(max([1-popularity_factor[movie],popularity_factor[movie]]))+tag_based_factor_weight*max([1-tag_based_factor[movie],tag_based_factor[movie]])
		recom_list[movie_title[movie]] = rating
	recom_list = sorted(recom_list.items(), key=operator.itemgetter(1), reverse=True)
	return recom_list

def sim_config(unrated_movie,movie_title,predicted_movie_rating,genre_factor,npmi_factor,popularity_factor,tag_based_factor):
	recom_list = {}
	for movie in unrated_movie:
		rating = predicted_movie_rating_weight*predicted_movie_rating[movie]+genre_factor_weight*(genre_factor[movie])+npmi_factor_weight*(npmi_factor[movie])+popularity_factor_weight*(popularity_factor[movie])+tag_based_factor_weight*(tag_based_factor[movie])
		recom_list[movie_title[movie]] = rating
	recom_list = sorted(recom_list.items(), key=operator.itemgetter(1), reverse=True)
	return recom_list

@hook('after_request')
def enable_cors():
	"""
	You need to add some headers to each request.
	Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
	"""
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route('/uid')
def uid():
	uid = request.query.uid
	config = request.query.config
	print(config)
	rated_movie_users,rated_movie,unrated_movie,predicted_movie_rating = knn.k_collab_filter_program_controller(starting_time,cursor,uid,no_of_rated_movies_fetch,no_of_users_fetch,no_of_unrated_movies,all_the_user_rating)
	# print("got predictrive rating",time.time()-starting_time)
	# time_elapsed_to_get_data_from_first_filter = time.time() - starting_time 

	#genre based content filter
	genre_factor = cbf.content_based_filter_controller(all_the_user_rating,rated_movie,unrated_movie,count_of_genre,movie_with_genre,cursor)
	# time_elapsed_to_get_data_from_second_filter = time.time() - starting_time
	print("startng npmi",time.time()-starting_time)
	#nmpi filter and popularity factor
	npmi_factor,popularity_factor = npmi.npmi_filter_program_controller(starting_time,all_the_user_rating,count_and_list_of_user_rated_movie,rated_movie,unrated_movie)
	print("npmi over",time.time()-starting_time)

	tag_based_factor = tbf.tag_based_filter_controller(tag_relav,movie_tag,rated_movie,unrated_movie)
	print("npmi over",time.time()-starting_time)
	
	dump = {}
	
	recom_list1 = dissim_config(unrated_movie,movie_title,predicted_movie_rating,genre_factor,npmi_factor,popularity_factor,tag_based_factor)
		
	recom_list2 = mixed_config(unrated_movie,movie_title,predicted_movie_rating,genre_factor,npmi_factor,popularity_factor,tag_based_factor)
	
	recom_list3 = sim_config(unrated_movie,movie_title,predicted_movie_rating,genre_factor,npmi_factor,popularity_factor,tag_based_factor)
	
	# print(recom_list1)
	# sim_recom = {}
	# mix_recom = {}
	# dissim_recom = {}
	# i=0
	# for movie in recom_list1:
	# 	print(movie)
	# 	sim_recom[movie] = recom_list1[movie]
	# 	i+=1
	# 	if(i>10):
	# 		break

	# i=0
	# for movie in recom_list2:
	# 	mix_recom[movie] = recom_list2[movie]
	# 	i+=1
	# 	if(i>10):
	# 		break

	# i=0
	# for movie in recom_list3:
	# 	dissim_recom[movie] = recom_list3[movie]	
	# 	i+=1
	# 	if(i>10):
	# 		break
	MAX_RESULTS = 10
	# print(dict(recom_list3[:MAX_RESULTS]))
	dump['sim_recom'] = dict(recom_list3[:MAX_RESULTS])

	dump['dissim_recom'] = dict(recom_list1[:MAX_RESULTS])

	dump['mix_recom'] = dict(recom_list2[:MAX_RESULTS])

	# print(dump)
	return json.dumps(dump)
###########---program starts here---###########

no_of_rated_movies_fetch = 200
no_of_users_fetch = 200
no_of_unrated_movies = 200

predicted_movie_rating_weight = .2
genre_factor_weight = .2
npmi_factor_weight = .2
popularity_factor_weight = .2
tag_based_factor_weight = .2 

password = getpass.getpass(prompt='enter the password - ')
# password = input("enter the password - ")

db = pymysql.connect("localhost","root",password,"newMovieLens" )
cursor = db.cursor()

starting_time = time.time()

movie_title = get_all_movie_title(cursor)

all_the_user_rating = get_all_the_rating_and_user(cursor)
# time_elapsed_to_get_user_data = time.time() - starting_time

movie_with_genre = get_movies_with_genre(cursor)
# time_elapsed_to_get_genre = time.time() - starting_time 

count_of_genre = get_the_count_of_genre(cursor)

tag_relav,movie_tag = get_tag_relav(cursor)

count_and_list_of_user_rated_movie = get_count_and_list_of_user_rated_movie(all_the_user_rating)
print(time.time()-starting_time)
#knn filter

run(host='localhost', port=8080, debug=True)
# collaborative_filter()