from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from math import pow,sqrt
from .forms import *



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

def get_similarity_pearson(user_a_id,user_b_id):

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
			
		if(deviation_a!=0 and deviation_b!=0):
			similarity = covariance/sqrt(deviation_a)*sqrt(deviation_b)
		else:
			similarity = 0	
	else:
		similarity=-1	
	return similarity
	
def get_similarity_cosine(user_a_id,user_b_id):
	user_a = User.objects.get(userid=user_a_id)
	user_b = User.objects.get(userid=user_b_id)
	
	movies_a = Rating.objects.filter(userid=user_a) 
	movies_b = Rating.objects.filter(userid=user_b)
	
	intersection = get_intersection(user_a,user_b)

	rating_a = []
	rating_b = []		
	cont = 0
	numerador = 0
	abs_value_a = 0
	abs_value_b = 0
	if(bool(intersection)==True):	
		for movie in intersection:			
			rating_a.append(get_rating(user_a,movie.movieid))
			rating_b.append(get_rating(user_b,movie.movieid))
			numerador += rating_a[cont]*rating_b[cont]
			abs_value_a += pow((rating_a[cont]),2)
			abs_value_b += pow((rating_b[cont]),2)
			cont+=1
		similarity = (numerador)/(sqrt(abs_value_a) * sqrt(abs_value_b))
	else:
		similarity=-1	
	return similarity

def similarity_test(request):
	print(get_similarity(1,19))
	return HttpResponse(get_similarity_pearson(1,19))

def get_prediction(user_id,movie_id):

	user_a = User.objects.get(userid=user_id)		
	rating_differences = 0
	similarities_sum = 0		
	if (Rating.objects.filter(userid=user_id,movieid=movie_id).exists()==False):
		movie_ratings = Rating.objects.filter(movieid=movie_id)
		for rating in movie_ratings:	
			user_b = User.objects.get(userid=rating.userid.userid)
			movies_b = Rating.objects.filter(userid=user_b.userid)		
			similarity_a_b = get_similarity_cosine(user_a.userid,user_b.userid)
			intersection = get_intersection(user_a,user_b)
			avg_rating_user_b = get_avg_movie(user_b,movies_b)				
			rating_differences += (similarity_a_b * (get_rating(user_b.userid,movie_id)- avg_rating_user_b))
			similarities_sum += similarity_a_b
		movies_a = 	Rating.objects.filter(userid=user_a.userid)
		avg_rating_user_a=get_avg_movie(user_a, movies_a)
		if(similarities_sum !=0 ):		
			prediction = avg_rating_user_a + (rating_differences/similarities_sum)
		else:
		 	prediction = 0	
		return prediction
	else:
		print("O usuário já viu o filme escolhido, por favor escolha outro.")

def prediction_test(request):
	print(get_prediction(1,3671))
	return HttpResponse(get_prediction(1,3671))		

def pre_process_predictions():
	users_that_rated_movies = Rating.get_list_users()
	rating = Rating()
	for user in users_that_rated_movies:
		unwatched_movies = rating.get_unwatched_movies(user.userid)
		for movie_id in unwatched_movies:
			prediction = get_prediction(user.userid,movie_id)
			movie = Movie.objects.get(movieid=movie_id)
			recommendation = Recommendation(userid=user,movieid=movie,prediction_rating=prediction)
			recommendation.save()	

def get_recommendation(userobj):
	recommendations =list(Recommendation.objects.filter(userid=userobj.userid).order_by('-prediction_rating'))
	for rec in recommendations:
		print(rec.prediction_rating)

def recommendation_view(request):
	if request.method == "POST":
		form = FormUser(request.POST)
		if form.is_valid():
			user = form.cleaned_data['name']
			get_recommendation(user)
			
	else:
		form = FormUser()
	return render(request, 'recommendation_user.html',{'form': form})