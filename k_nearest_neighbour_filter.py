import pymysql
import math

def list_contains_element(lis,element,column):
	for elem in lis:
		if(elem[column]==element):
			return True
	return False

#user A is the user for which we are trying to get the recommendation
def cal_avg_rating_of_user_A(uid,curosr):
	query = "select avg(rating) from orating where uid="+str(uid)
	cursor.execute(query)
	return cursor.fetchone()

#calculates the avg rating that the user who have seen the movies rated by user_A
def cal_avg_rating_of_users(rated_movie_users,all_the_user_rating):
	users_avg = {}
	for user in rated_movie_users:
		rat_sum = 0.
		i = 0
		for movie in all_the_user_rating[user]:
			rat_sum += float(all_the_user_rating[user][movie])
			i+=1
		avg = rat_sum/i
		users_avg[user] = avg

	return users_avg

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

#fetches movies that are rated by the user
def fetch_rated_movie(no_of_seen_movies_fetch,uid,cursor):
	query = "select * from orating where uid ="+ str(uid) +" order by rand() limit "+ str(no_of_seen_movies_fetch)
	cursor.execute(query)
	return cursor.fetchall()

#fetches the old user that have seen the most movies seen by user
def fetch_users(no_of_users_fetch,rated_movie,all_the_user_rating):
	no_of_movies_matched = []
	users_max_movie_watched = []
	for user in all_the_user_rating:
		i = 0
		for movie in rated_movie:
			if(movie[1] in all_the_user_rating[user]):
				i+=1
			
		no_of_movies_matched.append([user,i])
	
	no_of_movies_matched = sorted(no_of_movies_matched,key=lambda x: x[1],reverse=True)
	
	for i in range(0,no_of_users_fetch):
		users_max_movie_watched.append(no_of_movies_matched[i][0])

	#print(users_max_movie_watched)
	return users_max_movie_watched

#fetches movies that are not rated by the user
def fetch_unrated(no_of_unrated_movies,rated_movie_users,rated_movie,all_the_user_rating):
	unrated_movie = []
	i = 0
	#print(rated_movie_users)
	for user in rated_movie_users:
		#print(all_the_user_rating[user])
		for movie in all_the_user_rating.get(user):
			if(list_contains_element(rated_movie,movie,0)==False):
				i+=1
				unrated_movie.append(movie)
			if(i>no_of_unrated_movies):
				break
	return unrated_movie

#k_nearst_neigbour for finding the old users that are most similar to the user
def k_nearest_neighbour(uid,rated_movie,rated_movie_users,all_the_user_rating,cursor): 
	similarity = []
	user_a_avg = cal_avg_rating_of_user_A(uid,cursor)
	users_avg = cal_avg_rating_of_users(rated_movie_users,all_the_user_rating)
	
	numat = 0.
	denomat_left = 0.
	denomat_right = 0.

	for user in rated_movie_users:
		for movie in rated_movie:
			if(all_the_user_rating[user].get(movie[1])!=None):
				numat += (((float(movie[2])-float(user_a_avg[0]))*(float(all_the_user_rating[user].get(movie[1],users_avg[user]))-float(users_avg[user]))))
				denomat_left += pow((float(movie[2])-float(user_a_avg[0])),2)
				denomat_right += pow((float(all_the_user_rating[user].get(movie[1],users_avg[user]))-float(users_avg[user])),2)
		denomat = math.sqrt(denomat_left)*math.sqrt(denomat_right)
		if(denomat==0):
			sim = 0
		else:
			sim = numat/denomat

		similarity.append([user,sim])
	return similarity

def predict_movie_rating(unrated_movies_by_rated_movies_users,similarity_matrix):
	predicted_movie_rating = []
	for movie in unrated_movies_by_rated_movies_users:
		rating = 0.
		weight_sum = 0.
		for user in similarity_matrix:
			if(all_the_user_rating[user[0]].get(movie)!=None):
				rating += user[1]*float(all_the_user_rating[user[0]][movie])
				weight_sum += user[1]
		predicted_rating = rating/weight_sum
		predicted_movie_rating.append([movie,predicted_rating])
	return predicted_movie_rating

def k_collab_filter_program_controller(cursor,uid,no_of_rated_movies_fetch,no_of_users_fetch,no_of_unrated_movies,all_the_user_rating):
	rated_movie = fetch_rated_movie(no_of_rated_movies_fetch,uid,cursor)

	rated_movie_users = fetch_users(no_of_users_fetch,rated_movie,all_the_user_rating)

	unrated_movies_by_rated_movies_users = fetch_unrated(no_of_unrated_movies,rated_movie_users,rated_movie,all_the_user_rating)

	similarity_matrix = k_nearest_neighbour(uid,rated_movie,rated_movie_users,all_the_user_rating,cursor)

	similarity_matrix = sorted(similarity_matrix,key=lambda x: x[1],reverse=True)

	predicted_movie_rating = predict_movie_rating(unrated_movies_by_rated_movies_users,similarity_matrix)

	predicted_movie_rating = sorted(predicted_movie_rating,key=lambda x: x[1],reverse=True)

	return predicted_movie_rating
############---testing k_nearest_function---#############

#setting the first user for testing purpose
uid = 1
no_of_rated_movies_fetch = 200
no_of_users_fetch = 200
no_of_unrated_movies = 200

password = input("enter the password - ")

db = pymysql.connect("localhost","root",password,"newMovieLens" )
cursor = db.cursor()
all_the_user_rating = get_all_the_rating_and_user(cursor)
k_collab_filter_program_controller(cursor,uid,no_of_rated_movies_fetch,no_of_users_fetch,no_of_unrated_movies,all_the_user_rating)