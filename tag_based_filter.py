import math

def tag_based_filter(tag_relav,movie_tag,rated_movie,unrated_movie):
	tag_based_factor = []
	for unrat_movie in unrated_movie:
		i = 0
		factor = 0
		if(unrat_movie in tag_relav):
			j=0
			unrat_j = 0
			rat_j = 0
			temp = 0
			for rat_movie in rated_movie:
				if(rat_movie in tag_relav):
					i+=1
					tag = movie_tag[unrat_movie]&movie_tag[rat_movie]
					for ta in tag:
						temp += tag_relav[unrat_movie][ta]*tag_relav[rat_movie][ta]
						j +=1
						# rat_j += tag_relav[rat_movie][ta]
						# unrat_j += tag_relav[unrat_movie][ta]
				if(temp!=0):
					temp /= j
					# temp /= rat_j*unrat_j
				factor += temp
		if(i!=0):
			factor /= i
		tag_based_factor.append([unrat_movie,factor])

	return tag_based_factor

def tag_based_filter_controller(tag_relav,movie_tag,rated_movie,unrated_movie):
	return tag_based_filter(tag_relav,movie_tag,rated_movie,unrated_movie)