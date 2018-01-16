from django.conf.urls import url

from . import views

app_name = 'tournaments'
urlpatterns = [
    url(r'^$', views.TournamentsView.as_view(), name='tournaments'),
    url(r'^(?P<pk>[0-9]+)/$', views.TournamentDetailView.as_view(), name='details'),
    url(r'^new/$', views.createTournament, name='create_tournament'),
    url(r'^search/$', views.searchTournament, name='search_tournament'),
    url(r'^apllications/$', views.teamApplications, name='team_applications'),
    url(r'^apply/$', views.teamApply, name='team_apply')
]
