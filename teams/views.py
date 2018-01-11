import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User

from teams.models import Team, TeamMembers

class TeamsView(generic.ListView):
    template_name = 'teams/teams.html'
    context_object_name = 'user_teams'

    def get_queryset(self):
        """Return teams, in which current user is registered."""
        team_member = Team.objects.filter(teammembers__user=self.request.user)
        team_founder = Team.objects.filter(founder=self.request.user)
        teams = team_member | team_founder
        return teams

def createTeam(request):
    """
    Create team model and save given data from AJAX form and redirect to its
    detail view.
    """
    if request.method == 'POST':
        team_name = request.POST['team-name']
        team_abbr = request.POST['team-abbr']
        user = request.user
        status = 1
        message = 'Ok'
        if (not Team.objects.filter(name=team_name).exists()):
            team = Team.objects.create(
                founder = user,
                name = team_name,
                abbreviaton = team_abbr)
            url = reverse('teams:details', args=(team.id,))
        else:
            status = 0
            message = 'Team name already registered, please choose another.'
            url = None
    response = {'status': status, 'message': message, 'url': url}
    return HttpResponse(json.dumps(response), content_type='application/json')

def addMembers(request):
    #TODO: create invitation member adding system
    """
    add given member to the given team.
    """
    if request.method == 'POST':
        member_name = request.POST['member-name']
        team_id = request.POST['team-pk']
        current_user = request.user
        team = Team.objects.get(pk=team_id)
        status = 1
        message = 'User successfully added to the team'
        if (team.founder == current_user):
            #TODO: user DoesNotExist exception
            try:
                new_member_user = User.objects.get(username=member_name)
                if (not team.teammembers_set.filter(user=new_member_user)):
                    team.teammembers_set.create(user=new_member_user)
                else:
                    status = 0
                    message = "User already added to team"
            except User.DoesNotExist:
                status = 0
                message = "User does not exist."
        else:
            status = 0
            message = 'Not authorized for this action.'

    response = {'status': status, 'message': message}
    return HttpResponse(json.dumps(response), content_type='application/json')

class TeamDetailView(generic.DetailView):
    model = Team
    template_name = 'teams/details.html'
