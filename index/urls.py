
from django.conf.urls import url
from index import views


urlpatterns = [
    url(r'^all_game/$', views.all_game, name="all_game"),
    url(r'^json_index_body_table/$', views.json_index_body, name="json_index_body"),
    url(r'^json_all_game_html/$', views.json_all_game_html, name="json_all_game_html"),
    url(r'^statistica/$', views.statistica, name="statistica"),
    url(r'^$', views.index, name="index"),
]