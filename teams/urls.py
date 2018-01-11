from django.conf.urls import url

from . import views

app_name = 'teams'
urlpatterns = [
    url(r'^$', views.TeamsView.as_view(), name='teams'),
    url(r'^new/$', views.createTeam, name='create_team'),
    url(r'^(?P<pk>[0-9]+)/$', views.TeamDetailView.as_view(), name='details'),
    url(r'^addmember/$', views.addMembers, name='add_members')
]
