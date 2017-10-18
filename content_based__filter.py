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



def content_based_filter(movie_with_genre,rated_movie,unrated_movie):
	no_of_genre_watched = []
	for unrate_movie in unrated_movie:
		i = 0
		for genre in movie_with_genre[unrate_movie]:
			for rat_movie in rated_movie:
				if(genre in movie_with_genre[rat_movie[1]]):
					i += 1
					break
		no_of_genre_watched.append([unrate_movie,i])
	return no_of_genre_watched

#there can be a improvement in this like i was thinking why are we diving the watched genre by total genre
#instead cab we divide it by total genre of the particular movie
def calculate_damping_factor(count_of_genre,no_of_genre_watched):
	damping_factor = []
	for movie in no_of_genre_watched:
		factor = movie[1]/count_of_genre
		damping_factor.append([movie[0],factor])
	return damping_factor

	
def content_based_filter_controller(all_the_user_rating,rated_movie,unrated_movie,count_of_genre,movie_with_genre,cursor):
	
	no_of_genre_watched = content_based_filter(movie_with_genre,rated_movie,unrated_movie)

	return calculate_damping_factor(count_of_genre,no_of_genre_watched)




########## testing contetn based filter
# uid = 1
# no_of_rated_movies_fetch = 200
# no_of_users_fetch = 200
# no_of_unrated_movies = 200

# password = input("enter the password - ")

# db = pymysql.connect("localhost","root",password,"newMovieLens" )
# cursor = db.cursor()
# all_the_user_rating = get_all_the_rating_and_user(cursor)

# content_based_filter_controller(all_the_user_rating,cursor)
