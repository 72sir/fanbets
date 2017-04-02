
from django.conf.urls import url
from index import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^all_game/$', views.all_game, name="all_game"),
]