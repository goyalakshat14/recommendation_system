import pymysql
import math
import time
import operator
def list_contains_element(lis,element,column):
	for elem in lis:
		if(elem[column]==element):
			return True
	return False

#user A is the user for which we are trying to get the recommendation
#CAN_BE_improved
#sql query taking so much time
def cal_avg_rating_of_user_A(uid,cursor):
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

#fetches movies that are rated by the user
def fetch_rated_movie(no_of_seen_movies_fetch,uid,cursor):
	query = "select * from orating where uid ="+ str(uid) +" limit "+ str(no_of_seen_movies_fetch)
	cursor.execute(query)
	rated = cursor.fetchall()
	rated_movie = {rated[0][1]}
	for movie in rated:
		if(len(rated_movie)==0):
			rated_movie = {movie[1]}
		else:
			rated_movie.update({movie[1]})
	return rated,rated_movie

#fetches the old user that have seen the most movies seen by user
def fetch_users(no_of_users_fetch,rated_movie_rating,all_the_user_rating):
	no_of_movies_matched = []
	users_max_movie_watched = []
	for user in all_the_user_rating:
		i = 0
		for movie in rated_movie_rating:
			if(movie[1] in all_the_user_rating[user]):
				i+=1
			
		no_of_movies_matched.append([user,i])
	
	no_of_movies_matched = sorted(no_of_movies_matched,key=lambda x: x[1],reverse=True)
	
	for i in range(0,len(no_of_movies_matched)):
		users_max_movie_watched.append(no_of_movies_matched[i][0])
	#print(users_max_movie_watched)
	return users_max_movie_watched

#fetches movies that are not rated by the user
def fetch_unrated(no_of_unrated_movies,rated_movie_users,rated_movie,all_the_user_rating):
	unrated_movie = {}
	i = 0
	#print(rated_movie_users)
	for user in rated_movie_users:
		#print(all_the_user_rating[user])
		j=0
		for movie in all_the_user_rating.get(user):
			if(movie not in rated_movie and movie not in unrated_movie):
				i+=1
				j+=1
				if(len(unrated_movie)==0):
					unrated_movie = {movie}
				else:
					unrated_movie.update({movie})
			if(i>no_of_unrated_movies):
				return unrated_movie
			if(j>2):
				break

	

#k_nearst_neigbour for finding the old users that are most similar to the user
def k_nearest_neighbour(uid,rated_movie_rating,rated_movie_users,all_the_user_rating,cursor): 
	similarity = []
	user_a_avg = cal_avg_rating_of_user_A(uid,cursor)
	users_avg = cal_avg_rating_of_users(rated_movie_users,all_the_user_rating)
	
	numat = 0.
	denomat_left = 0.
	denomat_right = 0.

	for user in rated_movie_users:
		for movie in rated_movie_rating:
			if(movie[1] in all_the_user_rating[user]):
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

def predict_movie_rating(all_the_user_rating,unrated_movies_by_rated_movies_users,similarity_matrix):
	predicted_movie_rating = {}
	for movie in unrated_movies_by_rated_movies_users:
		rating = 0.
		weight_sum = 0.
		for user in similarity_matrix:
			if(movie in all_the_user_rating[user[0]]):
				rating += user[1]*float(all_the_user_rating[user[0]][movie])
				weight_sum += user[1]
		predicted_rating = rating/weight_sum
		predicted_movie_rating[movie] = predicted_rating/5
	return predicted_movie_rating

def k_collab_filter_program_controller(starting_time,cursor,uid,no_of_rated_movies_fetch,no_of_users_fetch,no_of_unrated_movies,all_the_user_rating):
	rated_movie_rating,rated_movie = fetch_rated_movie(no_of_rated_movies_fetch,uid,cursor)
	
	rated_movie_users = fetch_users(no_of_users_fetch,rated_movie_rating,all_the_user_rating)

	unrated_movies_by_rated_movies_users = fetch_unrated(no_of_unrated_movies,rated_movie_users,rated_movie,all_the_user_rating)

	
	similarity_matrix = k_nearest_neighbour(uid,rated_movie_rating,rated_movie_users,all_the_user_rating,cursor)
	# print("got the similarity",time.time()-starting_time)
	# similarity_matrix = sorted(similarity_matrix,key=lambda x: x[1],reverse=True)
	# print("got the similarity",time.time()-starting_time)
	predicted_movie_rating = predict_movie_rating(all_the_user_rating,unrated_movies_by_rated_movies_users,similarity_matrix)

	# predicted_movie_rating = sorted(predicted_movie_rating.items(), key=operator.itemgetter(1), reverse=True)
	# predicted_movie_rating = sorted(predicted_movie_rating,key=lambda x: x[1],reverse=True)


	return rated_movie_users,rated_movie,unrated_movies_by_rated_movies_users,predicted_movie_rating
############---testing k_nearest_function---#############

# #setting the first user for testing purpose
# uid = 1
# no_of_rated_movies_fetch = 200
# no_of_users_fetch = 200
# no_of_unrated_movies = 200

# password = input("enter the password - ")

# db = pymysql.connect("localhost","root",password,"newMovieLens" )
# cursor = db.cursor()

# all_the_user_rating = get_all_the_rating_and_user(cursor)
# k_collab_filter_program_controller(cursor,uid,no_of_rated_movies_fetch,no_of_users_fetch,no_of_unrated_movies,all_the_user_rating)