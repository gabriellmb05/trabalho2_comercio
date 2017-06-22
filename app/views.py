from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from math import pow,sqrt
from .forms import *
import json


def get_rating(user_id,movie_id):
    """Dado um id de usuário e um id de filme
    a função retorna a classificação que o usuário fez.
    """
    try:
        rating = Rating.objects.get(userid=user_id,movieid=movie_id)
        return rating.rating
    except:
        print ("Filme ou usuário inexistentes.")

def get_avg_movie(user,set_of_movies):
    """Dado um objeto User e uma lista de filmes a função
    retorna a média das classificações feitas pelo usuário.
    """
    sum_ratings=0
    for movie in list(set_of_movies):
        sum_ratings+=get_rating(user.userid,movie.movieid)

    return sum_ratings/len(set_of_movies)

def get_intersection(user_a,user_b):
    """Dado dois 2 id's de usuário a função retorna os
    um conjunto de id's dos filmes que ambos usuários classificaram.
    """
    rated_movies_user_a = list(Rating.objects.filter(userid= user_a.userid))
    rated_movies_user_b = list(Rating.objects.filter(userid= user_b.userid))

    set_rated_movies_user_a = set(rating.movieid for rating in rated_movies_user_a)
    set_rated_movies_user_b = set(rating.movieid for rating in rated_movies_user_b)

    intersection = set_rated_movies_user_a.intersection(set_rated_movies_user_b)

    return intersection

def get_similarity_pearson(user_a_id,user_b_id):
	"""Função responsável por calcular a similaridade entre dois usuários. Dado dois  id's de usuário a função retorna calcula	a
	similaridade entre os mesmos aplicando a formula de pearson, com base nos filmes que ambos os usuários assistiram. A variável
	covariancie acumula um somatório onde rating_a e rating_b são as classificações dos filmes que estão passando no loop e
	avg_rating_user_a e avg_rating_user_b a média das clássificações dos filmes dos usuários a e b. A variável deviation_a e
	deviation_b acumulam o desvio padrão dos usuários a e b. Caso a interceção seja vazia, significa que os usuários não possuem
	similaridade logo recebem o valor -1. Caso o desvio padrão de a ou b seja zero, significa que o valor da classificação e da média
	são iguais portanto tem similaridade 0 que é um valor neutro.
	"""
	user_a = User.objects.get(userid=user_a_id)
	user_b = User.objects.get(userid=user_b_id)

	movies_a = Rating.objects.filter(userid=user_a)
	movies_b = Rating.objects.filter(userid=user_b)

	intersection = get_intersection(user_a,user_b)

	covariance = 0
	deviation_a = 0
	deviation_b = 0

	if(bool(intersection)==True):
		avg_rating_user_a = get_avg_movie(user_a,intersection)
		avg_rating_user_b = get_avg_movie(user_b,intersection)
		for movie in intersection:
			rating_a = get_rating(user_a,movie.movieid)
			rating_b = get_rating(user_b,movie.movieid)
			covariance += ((rating_a-avg_rating_user_a)*(rating_b-avg_rating_user_b))
			deviation_a += pow((rating_a-avg_rating_user_a),2)
			deviation_b += pow((rating_b-avg_rating_user_b),2)

		if(deviation_a!=0 and deviation_b!=0):
			similarity = covariance/(sqrt(deviation_a)*sqrt(deviation_b))
		else:
			similarity = 0
	else:
		similarity=-1
	return similarity

def get_similarity_cosine(user_a_id,user_b_id):
    """Função responsável por calcular a similaridade entre dois usuários. Dado dois id's de usuário a função retorna
    calcula a similaridade entre os mesmos aplicando a formula da distância do cosseno,	com base nos filmes que ambos os usuários
    assistiram. A variável rating_a e rating_b são vetores de com as classificações para os filmes que foram vistos pelo usuário.
    Caso a interceção seja vazia, significa que os usuários não possuem similaridade logo recebem o valor -1.
    """
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
        print(rating_a)
        print(rating_b)
    else:
        similarity=-1
    return similarity

def similarity_test(request):
    print(get_similarity(1,19))
    return HttpResponse(get_similarity_pearson(1,19))

def get_prediction(user_id,movie_id):
    """Dado o id de um usuário e o id de um filme que ainda não foi visto a função faz uma predição se o usuário
    irá gostar do filme ou não. Essa função toma como base as classificações que todos os usuários fizeram para
    aquele filme e o grau de similaridade com o usuário passado como parametro para a função. Por fim aplica-se
    a formula de predição que consta nos slides do moodle. Caso o usuário não possua similaridade com nenhum outro
    a predição recebe o valor zero que é neutro.
    """
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
    """Função responsável por gerar uma tabela com as predições para os filmes
    não vistos pelos os usuários. Ela busca uma lista de usuários que já realizaram
    classificações, posteriormente faz um loop para cada um desses usuários realizando
    as predições para os filmes não vistos e salvando em uma tabela do banco de dados.
    """
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
    """Função responsável por retornar uma lista, ordenada de forma descente, com as recomendações
    para o usuário que estão acima da média de todas as recomendações já feitas.
    """
    avg_recommendation = Recommendation.avg_recommendation()
    recommendations =list(Recommendation.objects.filter(userid=userobj.userid, prediction_rating__gte=avg_recommendation).order_by('-prediction_rating'))

    return recommendations

def recommendation_view(request):
	recommended_movies=[]
	movies = Movie.objects.all()
	users = User.objects.all()
	movies_of_user = dict()
	movies_user_json = ''


	for user in users:
		movie_id = []
		movie_name = []
		user_json =dict()
		rating = Rating()
		watched_movies = rating.get_watched_movies(user.userid)
		for movie in watched_movies:
			movie_id.append(movie.movieid)
			movie_name.append(movie.title)
		user_json['movie_id'] = movie_id
		user_json['movie_title'] = movie_name

		movies_of_user[user.userid] = user_json

	movies_user_json = json.dumps(movies_of_user)
	if request.method == "POST":
		print('entrei post')
		if request.POST.get('btn-recommendation') == '1':
			form = FormUser(request.POST)
			if form.is_valid():
				user = form.cleaned_data['name']
				recommended_movies = get_recommendation(user)
				return render(request, 'recommended_movies.html', {'user':user,'recommendations':recommended_movies})
		elif(request.POST.get('btn-movie') == '0'):
			print('entrei 2')
			form_movie = FormMovieUser(request.POST)
			if form_movie.is_valid():
				user = form_movie.cleaned_data['users']
				movie = form_movie.cleaned_data['movies']
				rating = get_rating(user.userid, movie.movieid)
				return render(request, 'rating_movie.html', {'user':user,'movie':movie, 'rating':rating})
	else:
		form_user = FormUser()
		form_movie_user = FormMovieUser()
	return render(request, 'recommendation_user.html',{'form': form_user, 'form_movie':form_movie_user, 'json':movies_user_json})

def recommended_movies_user(request):
    return render(request, 'recommended_movies_user.html')

def get_intersection_user(movie1, movie2):
	rated_user_movie1 = list(Rating.objects.filter(movieid= movie1.movieid))
	rated_user_movie2 = list(Rating.objects.filter(movieid= movie2.movieid))

	set_rated_user_movie1 = set(rating.userid for rating in rated_user_movie1)
	set_rated_user_movie2 = set(rating.userid for rating in rated_user_movie2)

	intersection = set_rated_user_movie1.intersection(set_rated_user_movie2)

	return intersection

def get_similarity_cosine_item(movie1, movie2):
    """Função responsável por calcular a similaridade entre dois itens (Movie). Dado  2 objetos Movie a função retorna calcula
    a similaridade entre os mesmos aplicando a formula da distância do cosseno,	com base nos filmes que ambos os usuários assistiram.
    A variável rating_a e rating_b são vetores de com as classificações para os filmes que foram vistos pelo usuário. Caso a
    interceção seja vazia, significa que os usuários não possuem similaridade logo recebem o valor -1.
    """
    intersection = get_intersection_user(movie1, movie2)

    rating_a = []
    rating_b = []
    cont = 0
    numerador = 0
    abs_value_a = 0
    abs_value_b = 0
    if(bool(intersection)==True):
        for user in intersection:
            rating_a.append(get_rating(user,movie1.movieid))
            rating_b.append(get_rating(user,movie2.movieid))
            numerador += rating_a[cont]*rating_b[cont]
            abs_value_a += pow((rating_a[cont]),2)
            abs_value_b += pow((rating_b[cont]),2)
            cont+=1
            similarity = (numerador)/(sqrt(abs_value_a) * sqrt(abs_value_b))
        else:
            similarity=-1
        return similarity

def get_intersection_user(movie1, movie2):
    """Dado  2 objetos Movie a função retorna os
    um conjunto de id's de usuário classificaram os
    filmes passados por parametro.
    """
    rated_user_movie1 = list(Rating.objects.filter(movieid= movie1.movieid))
    rated_user_movie2 = list(Rating.objects.filter(movieid= movie2.movieid))

    set_rated_user_movie1 = set(rating.userid for rating in rated_user_movie1)
    set_rated_user_movie2 = set(rating.userid for rating in rated_user_movie2)

    intersection = set_rated_user_movie1.intersection(set_rated_user_movie2)

    return intersection

