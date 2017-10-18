
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

def get_movies_with_genre(cursor):
	query = "select * from genre"
	cursor.execute(query)
	print cursor.fetchall()

def content_based_filter();
	

#testing contetn based filter
uid = 1
no_of_rated_movies_fetch = 200
no_of_users_fetch = 200
no_of_unrated_movies = 200

db = pymysql.connect("localhost","root","tannugoyalU","newMovieLens" )
cursor = db.cursor()
all_the_user_rating = get_all_the_rating_and_user(cursor)
get_movies_with_genre(cursor)
