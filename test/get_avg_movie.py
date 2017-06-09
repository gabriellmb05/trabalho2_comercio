from app.views import *
from app.models import *
print("user_a:")
movies = Rating.objects.filter(userid=2)
print(len(movies))

avg = get_avg_movie(User.objects.get(userid=2),movies)

print(avg)

print("user_b:")
movies = Rating.objects.filter(userid=1)
print(len(movies))

avg = get_avg_movie(User.objects.get(userid=1),movies)

print(avg)