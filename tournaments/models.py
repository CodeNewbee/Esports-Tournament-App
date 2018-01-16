from django.db import models
from django.contrib.auth.models import User

from teams.models import Team

class Tournament(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    description = models.TextField()
    tournament_date = models.DateField()
    address = models.CharField(max_length=255)

class TournamentApplication(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

class TournamentTeams(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
