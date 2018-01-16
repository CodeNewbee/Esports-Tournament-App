from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    abbreviaton = models.CharField(max_length=4)

class TeamMembers(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, editable=True)
