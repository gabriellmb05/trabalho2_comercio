from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from math import pow,sqrt

def get_rating(user_id,movie_id):
	try:
		rating = Rating.objects.get(userid=user_id,movieid=movie_id)
		return rating.rating
	except:
		print ("Filme ou usuário inexistentes.")	
	
def get_avg_movie(user_id,set_of_movies):
	sum_ratings=0
	for movie in set_of_movies:
		sum_ratings+=get_rating(user_id,movie.movieid)

	return sum_ratings/len(set_of_movies)		

def get_similarity(user_a,user_b):
	try:
		user_a = User.objects.get(userid=user_a)
		user_b = User.objects.get(userid=user_b)

		rated_movies_user_a = list(Rating.objects.filter(userid= user_a.userid)) 
		rated_movies_user_b = list(Rating.objects.filter(userid= user_b.userid))

		set_rated_movies_user_a = set(rating.movieid for rating in rated_movies_user_a) 
		set_rated_movies_user_b = set(rating.movieid for rating in rated_movies_user_b) 	
		
		intersection = set_rated_movies_user_a.intersection(set_rated_movies_user_b)

		covariance = 0
		deviation_a = 0
		deviation_b = 0
		for movie in intersection:
			rating_a = get_rating(user_a,movie.movieid)
			rating_b = get_rating(user_b,movie.movieid)
			avg_rating_user_a = get_avg_movie(user_a,intersection)
			avg_rating_user_b = get_avg_movie(user_b,intersection)

			covariance += ((rating_a-avg_rating_user_a)*(rating_b-avg_rating_user_b))
			deviation_a += pow((rating_a-avg_rating_user_a),2)
			deviation_b += pow((rating_b-avg_rating_user_b),2)

		similarity = covariance/sqrt(deviation_a)*sqrt(deviation_b)
		return similarity
	except:
		print("Id do usuário inválida.")	
	

	def similarity_test(request):
		print(get_similarity(1,19))
		return HttpResponse(get_similarity(1,19))