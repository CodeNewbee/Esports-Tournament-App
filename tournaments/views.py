import json

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic

from tournaments.models import Tournament, TournamentApplication, TournamentTeams
from teams.models import Team

class TournamentsView(generic.ListView):
    """
    Generate tournaments view passing all registered tournaments.
    """
    template_name = 'tournaments/tournaments.html'
    context_object_name = 'tournaments'
    model = Tournament

def createTournament(request):
    """
    Create tournament model object and save.
    """
    if request.method == 'POST':
        name = request.POST['tournament-name']
        desc = request.POST['tournament-desc']
        date = request.POST['tournament-date']
        address = request.POST['tournament-address']
        organizer = request.user
        status = 1
        message = 'Ok'

        if (not Tournament.objects.filter(name=name).exists()):
            tournament = Tournament.objects.create(
                organizer = organizer,
                name = name,
                description = desc,
                tournament_date = date,
                address = address
            )
            url = reverse('tournaments:details', args=(tournament.id,))
        else:
            status = 0
            message = 'Tournament name already registered, please choose another'
            url = None
        response = {'status': status, 'message': message, 'url': url}
        return HttpResponse(json.dumps(response), content_type='application/json')

def searchTournament(request):
    """
    Find tournaments by name, render results view.
    """
    results = None
    if request.method == 'POST':
        query = request.POST['tournament-search']
        results = Tournament.objects.filter(name__contains=query)
    return render(request, 'tournaments/results.html', {'results': results})

def teamApplications(request):
    """
    Handle request to accept or deny team applications to join tournament.
    """
    status = 1
    message = "Successfully applied"
    if request.method == 'POST':
        team_ids = request.POST.getlist('team-applications[]')
        tournament_id = request.POST['tournament-id']
        button = request.POST.getlist('accept')
        for team_id in team_ids:
            team = Team.objects.get(id=team_id)
            tournament = Tournament.objects.get(id=tournament_id)
            tournamentapplication = TournamentApplication.objects.get(
                team = team,
                tournament = tournament
            )
            tournamentapplication.delete()
            if 'accept' in request.POST:
                tournament.tournamentteams_set.create(team=team)

    response = {'status': status, 'message': message}
    return HttpResponse(json.dumps(response), content_type='application/json')

def teamApply(request):
    """
    Handle request to apply for a tournament
    """
    status = 1
    message = "Successfully applied"
    if request.method == 'POST':
        team_ids = request.POST.getlist('teams[]')
        tournament_id = request.POST['tournament_id']
        for team_id in team_ids:
            team = Team.objects.get(id=team_id)
            tournament = Tournament.objects.get(id=tournament_id)
            tournament.tournamentapplication_set.create(team=team)
    response = {'status': status, 'message': message}
    return HttpResponse(json.dumps(response), content_type='application/json')

class TournamentDetailView(generic.TemplateView):
    template_name = 'tournaments/details.html'

    def get_context_data(self, **kwargs):
        """
        Return context with requested tournament and queryset of teams that current
        user is founder of and which aren't registered as accepted or applied teams.
        """
        context = super(TournamentDetailView, self).get_context_data(**kwargs)
        context['tournament'] = Tournament.objects.get(id=self.kwargs['pk'])
        context['teams'] = Team.objects.filter(
            founder=self.request.user
        ).exclude(
            tournamentapplication__team__id__in=TournamentApplication.objects.all().values_list('team__id')
        ).exclude(
            tournamentteams__team__id__in=TournamentTeams.objects.all().values_list('team__id')
        )
        return context
