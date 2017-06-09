from django.shortcuts import render
from .models import *
def get_rating(user_id,movie_id):
	try:
		rating = Rating.objects.get(userid=user_id,movieid=movie_id)
		return rating.rating
	except:
		print ("Filme ou usuário inexistentes.")	
	


