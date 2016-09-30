from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#, (REDIRECT_FIELD_NAME, logout as auth_logout)
from django.contrib import messages
import datetime
import calendar
import random
import re
import os

# Create your views here.

def login_user(request):
	return render(request, 'registration/login.html')

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

def authenticate_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('home', args=(user.id, )))
	else:
		return render(request, 'registration/login.html')

def new_user(request):
	return render(request, 'registration/new_user.html')

def create_user(request):
	new_user = User.objects.create_user(first_name=request.POST['first'], username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
	new_user.last_name = request.POST['last']
	new_user.save()
	return HttpResponseRedirect(reverse('home', args=(new_user.id, )))

@login_required()
def home(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	return render(request, 'marketplace/home.html')