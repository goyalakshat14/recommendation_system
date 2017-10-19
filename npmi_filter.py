import math
import time

def get_prob_rated_movie_user(count_and_list_of_user_rated_movie,total_users,rated_movie):
	prob_rated_movie_user = []
	for movie in rated_movie:
		prob_rated_movie_user.append(count_and_list_of_user_rated_movie[movie][0]/total_users)

	return prob_rated_movie_user

def get_prob_unrated_movie_user(count_and_list_of_user_rated_movie,total_users,unrated_movie):
	prob_unrated_movie_user = []
	for movie in unrated_movie:
		prob_unrated_movie_user.append(count_and_list_of_user_rated_movie[movie][0]/total_users)

	return prob_unrated_movie_user

#itertaing for each rated movie and seeing how many users have watched
#rated movie and unrated movie and store that accoridng to the unrated movie
#so that afterwards we can take the max of npmi of the max between unrated movies and a particular rated movie
def get_prob_user_watched_both(starting_time,count_and_list_of_user_rated_movie,total_users,rated_movie,unrated_movie):
	prob_user_watched_both = []
	for unrat_movie in unrated_movie:
		prob_watched_both = []
		pob = 0
		for rat_movie in rated_movie:
			user_watched_both = 0
			for user in count_and_list_of_user_rated_movie[unrat_movie][1]:
				# if(binary_search()):
				if(user in count_and_list_of_user_rated_movie[rat_movie][1]):
				#if(bina_search(count_and_list_of_user_rated_movie[rat_movie[1]][1],user)):
					user_watched_both += 1
			pob = user_watched_both
			prob_watched_both.append(user_watched_both/total_users)
		prob_user_watched_both.append(prob_watched_both)

	return prob_user_watched_both

#taking the avergae of the npmi so that we get avergae correaltion between
# the rated and unrated movies
def npmi_filter(prob_watched_rated_movie,prob_watched_unrated_movie_user,prob_user_watched_both):
	normalised_pointwise_mutual_info = []
	for index in range(0,len(prob_user_watched_both)):
		npmi = 0
		for rat_movie_index in range(0,len(prob_user_watched_both[index])):
			pmi = prob_user_watched_both[index][rat_movie_index]/(prob_watched_rated_movie[rat_movie_index]*prob_watched_unrated_movie_user[index])
			# print(prob_user_watched_both[index][rat_movie_index])
			# print((prob_watched_rated_movie[rat_movie_index]*prob_watched_unrated_movie_user[index]))
			# print("self something")
			# print((-math.log(prob_user_watched_both[index][rat_movie_index],2)))
			if(pmi==0):
				npmi += 0
			else:
				npmi += math.log(pmi,2)/(-math.log(prob_user_watched_both[index][rat_movie_index],2))
		normalised_pointwise_mutual_info.append(npmi/len(prob_user_watched_both[index]))

	return normalised_pointwise_mutual_info

def npmi_filter_program_controller(starting_time,all_the_user_rating,count_and_list_of_user_rated_movie,rated_movie,unrated_movie):
	total_users = len(all_the_user_rating)
	
	prob_watched_rated_movie = get_prob_rated_movie_user(count_and_list_of_user_rated_movie,total_users,rated_movie)

	prob_watched_unrated_movie_user = get_prob_unrated_movie_user(count_and_list_of_user_rated_movie,total_users,unrated_movie)

	print("getting both watched",time.time()-starting_time)
	prob_user_watched_both = get_prob_user_watched_both(starting_time,count_and_list_of_user_rated_movie,total_users,rated_movie,unrated_movie)
	print("got that",time.time()-starting_time)
	normalised_pointwise_mutual_info = npmi_filter(prob_watched_rated_movie,prob_watched_unrated_movie_user,prob_user_watched_both)

	return normalised_pointwise_mutual_info

	

	
# # testing collaborative filter

# password = input("enter the password - ")
# db = pymysql.connect("localhost","root",password,"newMovieLens" )
# cursor = db.cursor()