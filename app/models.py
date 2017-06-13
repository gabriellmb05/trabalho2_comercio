from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    movieid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    genres = models.CharField(max_length=200, blank=False)
    
    def __str__(self):
        return self.title
class Rating(models.Model):
    userid = models.ForeignKey(User, related_name='user_rating_fk')
    movieid =models.ForeignKey(Movie, related_name='movie_rating_fk') 
    rating = models.FloatField()

    def __str__(self):
        return str(self.userid)+" "+str(self.movieid)

    def get_list_users():
        list_users = []
        for rating in Rating.objects.all():
            user = rating.userid
            if(user not in list_users):
                list_users.append(user)                
        return list_users

    def is_movie_watched(self,userid,movieid):
        return Rating.objects.filter(userid=userid,movieid=movieid).exists()

    def get_unwatched_movies(self,userid):
        list_unwatched_movies = []
        for movie in Movie.objects.all():
            watched = self.is_movie_watched(userid,movie.movieid)
            if(not watched):
                list_unwatched_movies.append(movie.movieid)
        return list_unwatched_movies


class Recomendation(models.Model):
    userid = models.ForeignKey(User, related_name='user_prediction_fk')
    movieid =models.ForeignKey(Movie, related_name='movie_prediction_fk') 
    prediction_rating = models.FloatField()

    def __str__(self):
        return str(self.userid)+" "+str(self.movieid)