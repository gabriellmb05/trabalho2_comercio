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