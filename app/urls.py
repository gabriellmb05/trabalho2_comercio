from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^similarity/', get_similarity, name="get_similarity"),
]