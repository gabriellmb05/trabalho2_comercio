from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^similarity/', get_similarity_pearson, name="get_similarity"),
    url(r'^prediction/', get_prediction, name="get_prediction"),
    url(r'', recommendation_view, name="recommendation_view"),
    url(r'^recommendations/', recommended_movies_user, name="recommended_movies_user"),
]