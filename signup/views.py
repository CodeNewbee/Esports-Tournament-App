import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

def index(request):
    """
    Redirect to either authenticated index page or signup page depending if user
    is logged in or not.
    """
    if request.user.is_authenticated:
        return render(request, 'signup/home.html')
    else:
        return render(request, 'signup/signup.html')

def signup(request):
    """
    Create user using data received from AJAX form and redirect to authenticated
    user index page
    """
    #TODO more rigurous validation (password len, etc)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_conf = request.POST['password-conf']
        status = 1
        message = "Ok"
        url = reverse('home')

        if password == password_conf:
            try:
                user = User.objects.create_user(username, password=password)
            except IntegrityError:
                status = 0
                message = "Username already registred."
            if user is not None and status is 1:
                login(request, user)
        else:
            status = 0
            message = "Passwords dont match."

        response = {'status': status, 'message': message, 'url': url}
        return HttpResponse(json.dumps(response), content_type='application/json')

def logout_view(request):
    """
    Log a user out and redirect to index
    """
    logout(request)
    return redirect(index)

def login_view(request):
    """
    Log user on and redirect to logged in homepage.
    """
    username = request.POST['username']
    password = request.POST['password']
    status = 1
    message = "Ok"
    url = reverse('home')
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
    else:
        status = 0
        message = "Login failed. Check your username and password."
    response = {'status': status, 'message': message, 'url': url}
    return HttpResponse(json.dumps(response), content_type='application/json')

def home(request):
    """
    Go to logged in user homepage view
    """
    return render(request, 'signup/home.html')
