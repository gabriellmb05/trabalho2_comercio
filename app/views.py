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
	
def get_avg_movie(user,set_of_movies):
	sum_ratings=0		
	for movie in list(set_of_movies):				
		sum_ratings+=get_rating(user.userid,movie.movieid)

	return sum_ratings/len(set_of_movies)		

def get_intersection(user_a,user_b):
	rated_movies_user_a = list(Rating.objects.filter(userid= user_a.userid)) 
	rated_movies_user_b = list(Rating.objects.filter(userid= user_b.userid))

	set_rated_movies_user_a = set(rating.movieid for rating in rated_movies_user_a) 
	set_rated_movies_user_b = set(rating.movieid for rating in rated_movies_user_b) 	
	
	intersection = set_rated_movies_user_a.intersection(set_rated_movies_user_b)
	
	return intersection

def get_similarity(user_a_id,user_b_id):

	user_a = User.objects.get(userid=user_a_id)
	user_b = User.objects.get(userid=user_b_id)
	
	movies_a = Rating.objects.filter(userid=user_a) 
	movies_b = Rating.objects.filter(userid=user_b)
	
	intersection = get_intersection(user_a,user_b)
	
	covariance = 0
	deviation_a = 0
	deviation_b = 0
	
	if(bool(intersection)==True):	
		for movie in intersection:
			rating_a = get_rating(user_a,movie.movieid)
			rating_b = get_rating(user_b,movie.movieid)			
			avg_rating_user_a = get_avg_movie(user_a,movies_a)
			avg_rating_user_b = get_avg_movie(user_b,movies_b)			
			covariance += ((rating_a-avg_rating_user_a)*(rating_b-avg_rating_user_b))
			deviation_a += pow((rating_a-avg_rating_user_a),2)
			deviation_b += pow((rating_b-avg_rating_user_b),2)
			

		similarity = covariance/sqrt(deviation_a)*sqrt(deviation_b)
	else:
		similarity=-1	
	return similarity
	
	

def similarity_test(request):
	print(get_similarity(1,19))
	return HttpResponse(get_similarity(1,19))

def get_prediction(user_id,movie_id):

	user_a = User.objects.get(userid=user_id)		
	rating_differences = 0
	similarities_sum = 0	
	if (Rating.objects.filter(userid=user_id,movieid=movie_id).exists()==False):
		for rating in Rating.objects.filter(movieid=movie_id):	
			user_b = User.objects.get(userid=rating.userid.userid)
			movies_b = Rating.objects.filter(userid=user_b.userid)		
			similarity_a_b = get_similarity(user_a.userid,user_b.userid)
			intersection = get_intersection(user_a,user_b)
			avg_rating_user_b = get_avg_movie(user_b,movies_b)				
			rating_differences += (similarity_a_b * (get_rating(user_b.userid,movie_id)- avg_rating_user_b))
			similarities_sum += similarity_a_b
		movies_a = 	Rating.objects.filter(userid=user_a.userid)
		avg_rating_user_a=get_avg_movie(user_a, movies_a)	
		prediction = avg_rating_user_a + (rating_differences/similarities_sum)
		return prediction
	else:
		print("O usuário já viu o filme escolhido, por favor escolha outro.")

def prediction_test(request):
	print(get_prediction(1,3671))
	return HttpResponse(get_prediction(1,3671))		